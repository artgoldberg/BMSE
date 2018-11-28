"""
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-01-30
:Copyright: 2018, Arthur Goldberg
"""
import unittest


class TestStringMethods(unittest.TestCase):

    # Try many of the most useful unit test assertions
    # See them at https://docs.python.org/3/library/unittest.html#assert-methods

    def test_demo_some_assert_methods(self):
        l = [3, 2, 8, 9]
        # l == l
        self.assertEqual(l, l)
        m = [3, 2, 8, 9]
        m.reverse()
        # l != m
        self.assertNotEqual(l, m)
        m.reverse()
        # l == m
        self.assertEqual(l, m)
        self.assertTrue(l == m)
        self.assertFalse(l is m)

        # 3 in l
        self.assertIn(3, l)
        # -2 not in l
        self.assertNotIn(-2, l)

        # test exception, in a context manager
        with self.assertRaises(IndexError):
            l[len(l)]

        # test exception, and check error message
        with self.assertRaises(ValueError) as context:
            raise ValueError("It cannot be")
        self.assertIn('cannot', str(context.exception))

        a = 7
        b = a - 1E-9
        # round(a-b, 7) == 0
        self.assertAlmostEqual(a, b)

        # re.search(s)
        data_dependent_string = "Today {} is greater than {}".format(a, b)
        self.assertRegex(data_dependent_string, "Today .* is greater than")

        # coverage pragma to exclude lines and code blocs from coverage analysis
        if False:   # pragma: no cover
            # unittest method that always fails
            self.fail("fail example")

if __name__ == '__main__':
    unittest.main()
