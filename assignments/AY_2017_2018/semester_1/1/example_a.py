'''Biomedical Software Engineering: BMI2002: Assignment 1

:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Date: 2017-09-24
:Copyright: 2017, Arthur Goldberg
'''
# Problem 1: 
# Write a program that evaluates whether some Python operators on some types satisfy
# the associative, commutative, or distributive properties.
# For example, are + and * associative and commutative for Python integers,
# and are they distributive together?

# Helpful examples:

# associative: (a op b) op c  =  a op (b op c)
# commutative: a op b  =  b op a
# distributive: a op2 (b op1 c)  =  (a op2 b) op1 (a op2 c)

# is + associative? analytically, we find yes
if 1 + (2 + 3) == (1 + 2) + 3:
    print('+ appears associative')
else:
    print("+ isn't associative")

# is * associative? analytically, we find yes
if 1 * (2 * 3) == (1 * 2) * 3:
    print('* appears associative')
else:
    print("* isn't associative")

# is + commutative? analytically, we find yes
if 2 + 3 == 3 + 2:
    print('+ appears commutative')
else:
    print("+ isn't commutative")

# is * commutative? analytically, we find yes
if 2 * 3 == 3 * 2:
    print('* appears commutative')
else:
    print("* isn't commutative")

# is * left distributive over +? analytically, we find yes
if 2 * (3 + 4)  ==  (2 * 3)  +  (2 * 4):
    print('* appears left distributive over +')
else:
    print("* isn't left distributive over +")

# is + left distributive over *? analytically, we find NO
if 2 + (3 * 4)  ==  (2 + 3)  *  (2 + 4):
    print('+ appears left distributive over *')
else:
    print("+ isn't left distributive over *")
