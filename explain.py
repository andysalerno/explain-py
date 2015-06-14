#!/usr/bin/env python3
import os
import sys
import subprocess
from ManParser import *

TMP_DIR = '/tmp/explain_tmp/'

def get_man(command):
    man_location = TMP_DIR + command
    if not os.path.exists(man_location):
        print("tmp file didn't exist")
        if not os.path.exists(TMP_DIR):
            print("tmp dir didn't exist")
            os.makedirs(TMP_DIR)
        with open(man_location, 'wb+') as f:
            try:
                f.write(subprocess.check_output(['man', command]))
            except subprocess.CalledProcessError:
                print("Failed to open man page for command: " + command)
                quit()
    return open(man_location, 'r')

def get_args(all_args):
    short_args = set()
    long_args = set()

    for it in all_args:
        if it.startswith('--'):
            long_args.add(it[2:].lower())
        elif it.startswith('-'):
            short_args.update(list(it[1:]))

    return short_args, long_args

if __name__ == "__main__":
    if len(sys.argv) < 2 or (sys.argv[1] == '-s' and len(sys.argv) < 4):
        print("Usage:\nfind by exact option (-t, -s, --author):\n\texplain [command] [args...]")
        print("general search, including description body:\n\texplain -s [command] [search term]")
        quit()

    command = None
    args = None
    mode = None
    query = None
    short_args, long_args = None, None
    if sys.argv[1] == '-s':
        # search mode
        command = sys.argv[2]
        query = sys.argv[3]
        mode = SEARCH
    else:
        # normal mode
        command = sys.argv[1]
        args = sys.argv[2:]
        mode = NORMAL
        short_args, long_args = get_args(args)

    man_file = get_man(command)

    man_parser = ManParser(man_file)

    if sys.argv[1] == '-s':
        man_parser.search(sys.argv[3])
    else:
        man_parser.explain(short_args, long_args)

    man_file.close()