import traceback

def a():
    print('hi')
    traceback.print_stack()

def b():
    a()

def c():
    b()

c()
