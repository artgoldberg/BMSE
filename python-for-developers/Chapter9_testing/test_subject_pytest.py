import unittest
from subject import Subject, Gender, XStatus


class TestSubject(unittest.TestCase):

    def setUp(self):
        self.good_data = ['18795', 'female', '2005-01-07', 'affected']
        print('setUp')

    def tearDown(self):
        print('tearDown')

    def test_f(self):
        self.assertFalse(True)

    def test_verify(self):
        self.assertFalse(Subject.verify(*self.good_data))
