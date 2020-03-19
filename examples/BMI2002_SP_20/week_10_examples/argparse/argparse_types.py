#!/anaconda3/bin/python3
""" Demonstrate argparse error checking

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-12-06
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
            All optional arguments
            Type
            File to read
            File to write
    """

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

        # 'type' can take any callable that takes a single string argument and returns the converted value:
        parser.add_argument('--integer', '-i', type=int, help='an integer')
        parser.add_argument('--float', '-f', type=float, help='a float')

        # 'action' specifies how the command-line arguments should be handled
        # 'store_true' and 'store_false' store the values True and False respectively,
        # & create defaults of False and True respectively
        parser.add_argument('--flag', action='store_true', help='a true flag')
        parser.add_argument('--flag_false', action='store_false', help='a false flag')

        # argparse.FileType is a factory that opens files and takes open()'s arguments
        parser.add_argument('--outfile', type=argparse.FileType('w'))
        parser.add_argument('--infile', type=argparse.FileType('r'))
        parser.add_argument('--infile2', type=argparse.FileType('r'), default=sys.stdin, nargs='?')

        # 'type' can be any function taking a string that returns a value on success or raises argparse.ArgumentTypeError otherwise
        parser.add_argument('--identifier', type=ArgparseDemo.identifier, help='a Python identifier')
        print(parser.parse_args())

if __name__ == '__main__':

    ArgparseDemo.arg_types()
