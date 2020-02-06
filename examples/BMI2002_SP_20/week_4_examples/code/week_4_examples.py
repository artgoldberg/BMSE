'''
Advanced Python: lambda, map & comprehensions; yield & generators; eval & tokenize
'''
# a lambda expression is an anonymous function with parameters and a single expression
# a lambda behaves like a function object defined with:
# def <lambda>(parameters):
#     return expression
# https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
# since it doesn't have a name, it needs to be used where it's defined
# e.g.
pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
print(sorted(pairs, key=lambda pair: pair[1]))

# better
from collections import namedtuple
NamedTupleExample = namedtuple('NamedTupleExample', 'numeral name')
pairs = [NamedTupleExample(1, 'one'), NamedTupleExample(2, 'two'), NamedTupleExample(3, 'three')]
# avoid unnamed 1 index
print(sorted(pairs, key=lambda pair: pair.name))

# alternatively, an improved namedtuple
# see https://www.python.org/dev/peps/pep-0557/
# New in version 3.7
from dataclasses import dataclass

@dataclass
class Pair:
    ''' Class for example pair '''
    numeral: int
    name: str

pairs = [Pair(1, 'one'), Pair(2, 'two'), Pair(3, 'three'), Pair(4, 'four')]
print(sorted(pairs, key=lambda pair: pair.name))

# lambda's helpful with filter(), map(), etc.
# see https://docs.python.org/3/library/functions.html

# filter: https://docs.python.org/3/library/functions.html#filter
# filter(function, iterable)
@dataclass
class Person:
    ''' Class for example person '''
    name: str
    age: float

people = [Person('Ruby', 24), Person('Amelia', 22), Person('Bennett', 60)]
print(list(filter(lambda person: person.age < 30, people)))
# why do I wrap filter in list()?
print(list(filter(lambda person: 24 <= person.age and 'B' in person.name, people)))

# map: https://docs.python.org/3/library/functions.html#map
# map(function, iterable, ...)
print(list(map(lambda person: f"{person.name} Goldberg", people)))
print(list(map(lambda person, num: (f"{person.name} Goldberg", num+1), people, range(len(people)))))

# comprehensions:
# https://docs.python.org/3/tutorial/datastructures.html
# https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries
N_SQUARES = 6
eg = list(map(lambda x: x**2, range(N_SQUARES)))
print(eg)
# list comprehensions
eg = [x**2 for x in range(N_SQUARES)]
print(eg)
# list of tuples
eg = [(x, x**2) for x in range(N_SQUARES)]
print(eg)
# nested for comprehensions with if clause
N_INTS = 4
combinations = [(i, j) for i in range(N_INTS) for j in range(N_INTS) if i != j]
print(combinations)
# outer variables are available in inner loops
combinations = [f"x={x}, y={y}" for x in range(N_INTS) for y in range(x, x+N_INTS)]
print(combinations)
# and they don't leak into the outer scope
try:
    ([x for x in range(N_INTS)], x)
except NameError as e:
    print(e)

# comprehensions can make sets, too
eg = {x*x for x in range(N_INTS)}
print(eg)

# and comprehensions can make dictionaries
eg = {x: x**2 for x in range(N_SQUARES)}
print(eg)
eg = dict(zip(range(N_SQUARES), [x**2 for x in range(N_SQUARES)]))
print(eg)
