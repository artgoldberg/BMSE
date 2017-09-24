'''Biomedical Software Engineering: BMI2002: Assignment 1

:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Date: 2017-09-24
:Copyright: 2017, Arthur Goldberg
'''
# Problem 2:
# Write a program that systematically evaluates the associative and commutative properties of
# +, -, *, and / for integers, and the distributive for every pair of them.
# Also evaluate the associative and commutative properties of or and and for Booleans. 

# Helpful examples:

# Demonstrate Python eval().
print(eval("1+2"))
print(eval("2*3+4/5"))

# raises SyntaxError exception; try it
# print(eval(" 1  + 3-2)"))

# Demonstrate string format
i = 4
s = 'test'
print("i: {}; s: '{}'".format(i, s))

def single_operator_properties(operators):
    # test associative and commutative properties for integers
    for operator in operators:

        # associative?
        left_hand_side = "2 {} (3 {} 4)".format(operator, operator)
        right_hand_side = "(2 {} 3) {} 4".format(operator, operator)
        if eval(left_hand_side) == eval(right_hand_side):
            print("{} appears associative".format(operator))
        else:
            print("{} isn't associative".format(operator))

        # commutative?
        if eval("3 {} 4".format(operator, operator)) == eval("4 {} 3".format(operator, operator)):
            print("{} appears commutative".format(operator))
        else:
            print("{} isn't commutative".format(operator))

single_operator_properties(['+', '-', '*', '/'])
