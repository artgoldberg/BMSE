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
            Required vs. optional arguments
    """

    @staticmethod
    def req_vs_opt_args():
        parser = argparse.ArgumentParser(
            description='Demonstrate argparse error checking: required vs. optional args')
        parser.add_argument('an_int', type=int, help='a required integer')
        parser.add_argument('--str', '-s', type=str, help='an optional string')
        args = parser.parse_args()
        print(args.an_int, args.str)
        print(args)

if __name__ == '__main__':

    ArgparseDemo.req_vs_opt_args()
