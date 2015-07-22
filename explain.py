#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

from ManParser import *

TMP_DIR = '/tmp/explain_tmp/'

USAGE = '''Usage:
        To explain what a command will do:
        explain-py [command] [args...]
        To search for a command whose description contains QUERY:
        explain-py -s [command] [search terms...]'''


def get_man(command):
    man_location = TMP_DIR + command
    if not os.path.exists(man_location):
        if not os.path.exists(TMP_DIR):
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


def parse_arguments():
    raw_args = sys.argv
    parser = argparse.ArgumentParser(description="Print out relevant chunks of a command's man page for easy browsing.")
    parser.add_argument("-s", help="search bodies instead of titles", action="store_true")
    parser.add_argument("command", help="the command, for example: ls, tar, cp, ssh")
    parser.add_argument("command-args", nargs='?', help="the arguments that you would like to lookup")

    args = parser.parse_known_args()[0]
    mode = SEARCH if raw_args[1] == '-s' else EXPLAIN
    if mode == SEARCH:
        command_args = sys.argv[3:]
    else:
        command_args = sys.argv[2:]
    return args.command, command_args, mode


def main():
    command, args, mode = parse_arguments()

    man_file = get_man(command)
    man_parser = ManParser(man_file)

    if mode == SEARCH:
        man_parser.search(args)
    else:
        short_args, long_args = get_args(args)
        man_parser.explain(short_args, long_args)

    man_file.close()


if __name__ == "__main__":
    main()
