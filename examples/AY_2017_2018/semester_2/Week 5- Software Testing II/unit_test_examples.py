"""
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-01-30
:Copyright: 2018, Arthur Goldberg
"""
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('bmse'.upper(), 'BMSE')

    def test_isupper(self):
        self.assertTrue('BMSE'.isupper())
        self.assertFalse('Arthur'.isupper())

class TestStringMethodsException(unittest.TestCase):

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is an int
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
