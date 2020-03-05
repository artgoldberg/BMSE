"""
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2020-03-05
"""

# Illustrate Capture output and warnings

from capturer import CaptureOutput


with CaptureOutput() as capturer:
    # Generate some output from Python.
    print("Output from Python")
    # Each of these methods gets the output.
    assert capturer.get_bytes() == b'Output from Python\r\n'
    assert capturer.get_lines() == [u'Output from Python']
    assert capturer.get_text() == 'Output from Python'

# use in unittest
import sys
import unittest
import warnings


def f(text):
    print(text)


class TestF(unittest.TestCase):

    def test_f(self):
        # relay decides whether the output is sent to the stream; it's False by default
        with CaptureOutput(relay=False) as capturer:
            test_text = 'test text'
            f(test_text)
        self.assertEqual(capturer.get_text(), test_text)

        with CaptureOutput(relay=False) as capturer:
            test_text = 'test text'
            f('random text ' + test_text + ' more random text')
        # often, assertIn is simpler & more robust
        self.assertIn(test_text, capturer.get_text())

        # both stdout and stderr are captured
        with CaptureOutput() as capturer:
            test_text = 'test text'
            print(test_text, file=sys.stderr)
        self.assertIn(test_text, capturer.get_text())

    # note: capturer is fragile, because when other parts of code turn on or off output, capturer can be fooled

class CustomWarning(UserWarning):
    """ custom warning """
    pass


def g():
    warnings.warn("Warning: COVID-19 found", CustomWarning)


class TestG(unittest.TestCase):

    def test_g(self):
        with warnings.catch_warnings(record=True) as w:
            g()
            self.assertIn("COVID-19 found", str(w[-1].message))
