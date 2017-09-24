# For example, are + and * associative and commutative for Python integers, and is the pair of them distributive?

# associative: (a op b) op c  =  a op (b op c)
# commutative: a op b  =  b op a
# distributive: a op2 (b op1 c)  =  a op2 b  op1  a op2 c

# + associative? we expect yes
if 1 + (2 + 3) == 1 + (2 + 3):
    print('+ appears associative')
else:
    print("+ isn't associative")

# * commutative? we expect yes
if 2 * 3 == 3 * 2:
    print('* appears associative')
else:
    print("* isn't associative")

# are + and * left distributive? we expect no
if 2 * (3 + 4)  ==  (2 * 3)  +  (2 * 4):
    print('* appears left distributive over +')
else:
    print("* isn't left distributive over +")

if 2 + (3 * 4)  ==  (2 + 3)  *  (2 + 4):
    print('+ appears left distributive over *')
else:
    print("+ isn't left distributive over *")
