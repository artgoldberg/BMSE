def print_people(people):
    for p in people:
        print('\t', p)

# create a Person Joe, and store it in the variable 'joe'
joe = Person('Joe', 'male')
# check joe's name
assert joe.name == 'Joe'

print('Joe self'); print_people(joe.ancestors(0))
print('Joe parents None'); print_people(joe.ancestors(1))
# create a Person Mary, and make her Joe's mother
joe.mother = Person('Mary', 'F')
print('Joe parents mother'); print_people(joe.ancestors(1))

maternal_gm = joe.mother.mother = Person('Agnes', 'female')
# create a Person Joe Sr., and make him Joe's father
joe.father = Person('Joe Sr.', 'male')
print('joe parents(): Mary, Joe Sr.'); print_people(joe.parents())

# create joe's paternal grandfather
joe.father.father = Person('Old Joe', 'male')
# create joe's maternal grandmother
maternal_gm.mother = Person('Maternal ggm', 'female')
print('joe.grandparents_structured(), Agnes, Old Joe'); print_people(joe.grandparents_structured())
print('joe.grandparents(), Agnes, Old Joe'); print_people(joe.grandparents())
print('joe great-grandparents: Maternal ggm'); print_people(joe.great_grandparents())

# play with an infinite ancestry depth limit
inf = float('inf')
print('joes ancestors: Mary, Joe Sr., Agnes, Old Joe, Maternal ggm'); print_people(joe.all_ancestors())
print('joe and his ancestors'); print_people(joe.ancestors(0, inf))

# make Joe his mother's son
joe.mother.add_child(joe)
print('joe.mother.sons():'); print_people(joe.mother.sons())
print('joe.sons():', joe.sons())

kid = Person('kid', 'male', father=joe)
joe.add_child(kid)
