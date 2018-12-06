#!/anaconda3/bin/python3
""" Demonstrate argparse error checking

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-01-17
:Copyright: 2018, Arthur Goldberg
:License: MIT
"""

import argparse # see https://docs.python.org/3/library/argparse.html
import re, sys

class ArgparseDemo(object):
    """
        Kinds of arguments to parse:
            Required vs. optional arguments
            Argument type
            Documentation phrase for each argument
        Kinds of errors to check:
            Required vs. optional arguments
            Type
            File to read
            File to write
            Choice
    """

    @staticmethod
    def req_vs_opt_args():
        parser = argparse.ArgumentParser(description='Demonstrate argparse error checking: required vs. optional args')
        parser.add_argument('an_int', type=int, help='a required integer')
        parser.add_argument('--str', '-s', type=str, help='an optional string')
        print(parser.parse_args())

    @staticmethod
    def identifier(id):
        # Regular expression for valid Python identifiers
        identifier = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)
        result = re.match(identifier, id)
        if result is None:
            msg = "'{}' is not a Python identifier".format(id)
            raise argparse.ArgumentTypeError(msg)
        return id

    @staticmethod
    def arg_types():
        parser = argparse.ArgumentParser(description='Demonstrate argparse error checking: types')
        # type= can take any callable that takes a single string argument and returns the converted value:
        parser.add_argument('--integer', '-i', type=int, help='an integer')
        parser.add_argument('--float', '-f', type=float, help='a float')
        parser.add_argument('--outfile', type=argparse.FileType('w'))
        parser.add_argument('--infile', type=argparse.FileType('r'))
        parser.add_argument('--infile2', type=argparse.FileType('r'), default=sys.stdin, nargs='?')
        parser.add_argument('--identifier', type=ArgparseDemo.identifier, help='a Python identifier')
        parser.add_argument('--flag', action='store_true', help='a flag')
        parser.add_argument('--flag_false', action='store_false', help='a flag')
        print(parser.parse_args())

    @staticmethod
    def arg_choices():
        parser = argparse.ArgumentParser(description='Demonstrate argparse error checking: choices')
        parser.add_argument('move', choices=['rock', 'paper', 'scissors'], help='game choices')
        parser.add_argument('door', type=int, choices=range(1, 4), help="Let's make a deal choices")
        print(parser.parse_args())

if __name__ == '__main__':

    # ArgparseDemo.req_vs_opt_args()
    # ArgparseDemo.arg_types()
    ArgparseDemo.arg_choices()
    # argparse_demo = ArgparseDemo()