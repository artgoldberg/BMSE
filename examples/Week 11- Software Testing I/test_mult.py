import operator
from math import log2
import sys

inf = float('inf')
print(mul(3,2))
print(mul(2,'hi'))
print(mul([],{}))
#print(mul([],set()))
#print(mul([],'hi'))

print(mul(False,True))
print(mul(False,(1,3)))
print(mul(2,inf))
print(sys.maxsize, type(sys.maxsize))
print(mul(2,sys.maxsize), type(mul(2,sys.maxsize)))
print(mul(sys.maxsize,sys.maxsize), type(mul(sys.maxsize,sys.maxsize)))

# logs
print('log2s')
for v in [sys.maxsize, mul(2,sys.maxsize), mul(sys.maxsize,sys.maxsize), inf]:
    print(v, log2(v))

# basic idea
if mul(2,3) != 6:
    print('argh 2*3 != 6')

assert mul(2,3) == 6

# assert mul(2,3) == 7

# assert mul(2,3) == 7, 'good, mul(2,3) != 7'

try:
    assert mul(2,3) == 6, 'mul error, mul(2,3) != 6'
except AssertionError as e:
    print(e)
    
import random

'''
def mul(a,b):
    if b==7:
        return operator.mul(a,8)
    return operator.mul(a,b)
'''

max_rand_int = sys.maxsize
max_rand_int = 10


tries = 1000
def test_mul(tries):
    for i in range(tries):
        x = random.randrange(max_rand_int)
        assert mul(1,x) == x, "mul error: mul(1,{}) != {}".format(x, x)
        assert mul(0,x) == 0, "mul error: mul(0,{}) != 0".format(x)
        y = random.randrange(max_rand_int)
        assert mul(x,y) == mul(y,x), "mul error: mul({},{}) != mul({},{})".format(x, y, y, x)

