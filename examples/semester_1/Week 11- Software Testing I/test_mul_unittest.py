import unittest
from operator import mul 
import operator 
import random
            
def mul(a,b):
    if b==7:
        return operator.mul(a,8)
    return operator.mul(a,b)

# values of max_rand_int slightly larger than 7 will trigger test failures; big values rarely do
max_rand_int = 10000000

class TestMul(unittest.TestCase):

    def test_mul(self):
        self.assertEqual(mul(2,3), 6)

    def test_mul_props(self):
        tries = 1000
        for i in range(tries):
            x = random.randrange(max_rand_int)
            self.assertEqual(mul(1,x), x)
            self.assertEqual(mul(0,x), 0)
            y = random.randrange(max_rand_int)
            self.assertEqual(mul(x,y), mul(y,x))