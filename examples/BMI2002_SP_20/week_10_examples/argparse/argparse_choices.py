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
            Choice
    """

    @staticmethod
    def arg_choices():
        parser = argparse.ArgumentParser(description='Demonstrate argparse error checking: choices')
        parser.add_argument('move', choices=['rock', 'paper', 'scissors'], help='game choices')
        parser.add_argument('door', type=int, choices=range(1, 4), help="Let's make a deal choices")
        print(parser.parse_args())

if __name__ == '__main__':

    ArgparseDemo.arg_choices()
