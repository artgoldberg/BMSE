import stack_trace_eg
import unittest

class Test(unittest.TestCase):
    def test(self):
       self.assertEqual(0, stack_trace_eg.i('test x'))
