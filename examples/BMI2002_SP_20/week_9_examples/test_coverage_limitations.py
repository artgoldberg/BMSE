""" Week 9 examples: test coverage limitations
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2020-03-11
"""

from abc import ABCMeta
import abc
import unittest


### Indicating lines that cannot be executed: "# pragma: no cover" ###

# Example 1
# Some code is only reachable when launched from the command line
if __name__ == '__main__':
    print("__name__ == '__main__'") # pragma: no cover     # reachable only from command line
else:
    print("__name__ != '__main__'")

# Example 2
# Abstract methods in Abstract Base Classes (https://docs.python.org/3/library/abc.html) don't get executed
class ApplicationSimulationObjectInterface(object, metaclass=abc.ABCMeta): # pragma: no cover

    @abc.abstractmethod
    def send_initial_events(self, *args): pass

    @abc.abstractmethod
    def get_state(self): pass


class Eg(ApplicationSimulationObjectInterface):

    def send_initial_events(self, *args):
        print('sending event')

    def get_state(self):
        return(1)

# "# pragma: no cover" can modify a line or a block

# Example 3
# Question for students: what would be another example of code that couldn't be executed by a test program?

class TestApplicationSimulationObjectInterface(unittest.TestCase):

    def test(self):
        eg = Eg()
        eg.send_initial_events()
        eg.get_state()


### Branch coverage testing limitations ###

# Code to test
def f0(cond):
    # multi-line conditional
    if cond:
        return True
    else:
        return False

def f1(cond):
    # multi-line conditional, not tested
    if cond:
        x = 1
    if cond:
        return True
    else:
        return False

def f2(food):
    # single line conditional
    rv = ''
    if food: rv = 'eat'; rv += 'digest'
    return rv

def f3(fruit):
    # a conditional expression (sometimes called a “ternary operator”)
    # See https://docs.python.org/3/reference/expressions.html#conditional-expressions
    # structure: value_when_true if condition else value_when_false
    return 'Yes' if fruit.casefold() == 'apple' else 'No'


class TestBranchCoverageExamples(unittest.TestCase):

    def test_f0(self):
        self.assertEqual(f0(True), True)
        self.assertEqual(f0(False), False)

    def test_f1(self):
        # self.assertEqual(f1(True), True)
        self.assertEqual(f1(False), False)

    def test_f2(self):
        self.assertIn('eat', f2(True))
        # Question for students: what assert test can be added to test the branch being missed, but not reported by coverage?
        # possible answers
        self.assertEqual('', f2(False))
        self.assertNotIn('eat', f2(False))

    def test_f3(self):
        self.assertIn('Yes', f3('APPLE'))
        self.assertIn('Yes', f3('apple'))

    def test_f4(self):
        self.assertIn('Yes', f4('APPLE'))
        self.assertIn('Yes', f4('apple'))
        self.assertIn('No', f4('orange'))

# Currently, the only way to address these limitations of coverage is to convert the code into multi-line blocks
# E. g., rewrite f3 as:

def f4(fruit):
    if fruit.casefold() == 'apple':
        return 'Yes'
    return 'No'

