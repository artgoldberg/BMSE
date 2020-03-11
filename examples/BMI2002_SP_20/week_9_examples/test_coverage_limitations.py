"""
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
# Methods in superclasses that are not implemented and 
# Abstract methods in Abstract Base Classes (https://docs.python.org/3/library/abc.html) don't get executed
class ApplicationSimulationObjectInterface(object, metaclass=abc.ABCMeta):  # pragma: no cover

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

class TestApplicationSimulationObjectInterface(unittest.TestCase):

    def test_f1(self):
        eg = Eg()
        eg.send_initial_events()
        eg.get_state()


### Limitations and challenges of branch coverage testing ###

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


class TestCoverageExamples(unittest.TestCase):

    def test_f0(self):
        self.assertEqual(f0(True), True)
        self.assertEqual(f0(False), False)

    def test_f1(self):
        # self.assertEqual(f1(True), True)
        self.assertEqual(f1(False), False)
        pass

    def test_f2(self):
        self.assertIn('eat', f2(True))
        # Q: if this test is not run what branch is being missed, but not reported as missed?:
        # self.assertNotIn('eat', f2(False))

