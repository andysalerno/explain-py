import re

(NAME, DESCRIPTION, FOUND) = range(3)
(SEARCH, EXPLAIN) = range(2)


class ManParser:
    def __init__(self, man_file):
        self.man_iter = iter(man_file.readlines())

        self.mode = None
        self.name_checked = False
        self.state = None
        self.cur_line = None
        self.cur_example = ''

    def _advance(self):
        self.cur_line = next(self.man_iter, None)
        return self.cur_line

    def _act(self):
        if self.state == NAME:
            print(self.cur_line.rstrip(), end='\n')
            self.state = None

        elif self.mode == EXPLAIN and self.state == DESCRIPTION:
            if not self.cur_line.strip():
                self.state = None
            else:
                print(self.cur_line.rstrip(), end='\n')

    @staticmethod
    def _matches(cur_line, short_args, long_args):
        splitline = filter(None, re.split(',|;|\s', cur_line))
        for it in splitline:
            it = it.split('=')[0]
            if not it.startswith('-'):
                return False  # we stop looking for args the moment we see a non-arg
            elif it.startswith('--'):
                if it[2:].lower() in long_args:
                    return True
            elif it.startswith('-'):
                if it[1:] in short_args:
                    return True

    def explain(self, short_args, long_args):
        self.mode = EXPLAIN
        while self._advance():
            self._act()
            if not self.name_checked and self.cur_line.strip().lower() == 'name':
                self.state = NAME
                self.name_checked = True
            elif self._matches(self.cur_line, short_args, long_args):
                self.state = DESCRIPTION
                self._act()

    def search(self, query):
        self.mode = SEARCH
        while self._advance():
            self._act()
            splitline = self.cur_line.split()
            if not self.name_checked and len(splitline) == 1 and splitline[0].lower() == 'name':
                self.state = NAME
                self.name_checked = True
                continue

            if len(splitline) == 0:
                if self.state == FOUND:
                    print(self.cur_example.rstrip(), end='\n')
                self.cur_example = ''
                self.state = None
            elif splitline[0].startswith('-') and self.state != FOUND:
                self.state = DESCRIPTION

            if self.state == DESCRIPTION or self.state == FOUND:
                self.cur_example += self.cur_line

            if self.state == DESCRIPTION and query.lower() in self.cur_line.lower():
                self.state = FOUND
