from inspect import currentframe, getframeinfo

# frameinfo = getframeinfo(currentframe())
# print frameinfo.filename, frameinfo.lineno

import traceback

def f(x):
    print('in f')
    # traceback.print_stack()
    raise ValueError('x')

def g(x):
    print('in g')
    f(x)

def h(x):
    print('in h')
    g(x)

def i(x):
    print('in i')
    h(x)
    return 1


def foo(i):
    if i == 10:
        assert False
    if i<20:
        foo(i+1)

# foo(0)
