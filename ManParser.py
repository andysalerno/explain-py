import re

(NAME, DESCRIPTION, FOUND) = range(3)
(SEARCH, NORMAL) = range(2)

class ManParser:

    def __init__(self, man_file):
        self.man_iter = iter(man_file.readlines())

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

        elif self.state == DESCRIPTION:
            if not self.cur_line.strip():
                print()  # just print a newline
                self.state = None
            else:
                print(self.cur_line.rstrip(), end='\n')

    @staticmethod
    def _matches(cur_line, short_args, long_args):
        """
        Returns true if any char in short_args or any string in long_args is found in cur_line
        (only for the first words of cur_line that begin with a -)
        """
        splitline = filter(None, re.split(', |; |\s', cur_line))
        for it in splitline:
            it = it.split('=')[0]
            if not it.startswith('-'):
                # we stop looking for args the moment we see a non-arg
                return False
            elif it.startswith('--'):
                if it[2:].lower() in long_args:
                    return True
            elif it.startswith('-'):
                if it[1:] in short_args:
                    return True

    def explain(self, short_args, long_args):
        while self._advance():
            self._act()
            if self.cur_line.strip().lower() == 'name':
                self.state = NAME
            elif self._matches(self.cur_line, short_args, long_args):
                self.state = DESCRIPTION
                self._act()

    def search(self, query):
        while self._advance():
            splitline = self.cur_line.split()
            if len(splitline) == 0:
                if self.state == FOUND:
                    print(self.cur_example.rstrip(), end='\n\n')
                self.cur_example = ''
                self.state = None
            elif splitline[0].startswith('-') and self.state != FOUND:
                self.state = DESCRIPTION

            if self.state == DESCRIPTION or self.state == FOUND:
                self.cur_example += self.cur_line

            if self.state == DESCRIPTION and query.lower() in self.cur_line.lower():
                self.state = FOUND
