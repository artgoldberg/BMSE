""" Person, with heredity and other characteristics

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-10-12
:Copyright: 2017, Arthur Goldberg
:License: MIT
"""

class Person(object):
    """ Person

    Attributes:
        name (:obj:`str`): a person's name
        DOB (:obj:`str`): a person's date of birth
        gender (:obj:`str`): a person's gender
        mother (:obj:`Person`): a person's mother
        father (:obj:`Person`): a person's father
        children (:obj:list of `Person`): a person's children
    """
    def __init__(self, name, gender, mother=None, father=None):
        self.name = name
        self.gender = gender
        self.mother = mother
        self.father = father
        self.DOB = None
        self.children = []

    def get_persons_name(person):
        if person is None:
            return None
        return person.name

    def __str__(self):
        return "{}: DOB {}; gender {}; mother {}; father {}".format(
            self.name,
            self.DOB,
            self.gender,
            Person.get_persons_name(self.mother),
            Person.get_persons_name(self.father))

    def grandparents(self):
        ''' Provide grandparents

        Return 4-tuple:
            (maternal grandmother, maternal grandfather, paternal grandmother, paternal grandfather)
        Missing individuals identified by `None`.
        '''
        grandparents = []
        if self.mother:
            grandparents.extend([self.mother.mother, self.mother.father])
        else:
            grandparents.extend([None, None])
        if self.father:
            grandparents.extend([self.father.mother, self.father.father])
        else:
            grandparents.extend([None, None])
        return tuple(grandparents)

    def sons(self):
        sons = []
        for child in self.children:
            # TODO: standardize genders
            if child.gender == 'male':
                sons.append(child)
        return sons

    def add_child(self, person):
        self.children.append(person)

    def ancestors(self, min_depth, max_depth=None):
        # collect ancestors whose depth satisfies min_depth <= depth <= max_depth. Thus,
        # a person's parents and grandparents would have min_depth = 1 and max_depth = 2
        # returns a set
        if max_depth is not None:
            if max_depth < min_depth:
                    raise ValueError("max_depth ({}) cannot be less than min_depth ({})".format(
                        max_depth, min_depth))
        else:
            # collect just one depth
            max_depth = min_depth
        collected_ancestors = set()
        return self._ancestors(collected_ancestors, min_depth, max_depth)

    def _ancestors(self, collected_ancestors, min_depth, max_depth):
        # private, recursive ancestors method
        if min_depth <= 0:
            collected_ancestors.add(self)
        if 0 < max_depth:
            for parent in [self.mother, self.father]:
                if parent is not None:
                    parent._ancestors(collected_ancestors, min_depth-1, max_depth-1)
        return collected_ancestors

    def grandparents_simple(self):
        return self.ancestors(2)

    def parents_simple(self):
        return self.ancestors(1)

def print_people(people):
    for p in people:
        print('\t', p)

joe = Person('Joe', 'male')
assert joe.name == 'Joe'
joe.DOB = '2000-10-12'

print('Joe self'); print_people(joe.ancestors(0))
print('Joe parents None'); print_people(joe.ancestors(1))
joe.mother = Person('Mary', 'F')
print('Joe parents mother'); print_people(joe.ancestors(1))

maternal_gm = joe.mother.mother = Person('Agnes', 'female')
joe.father = Person('Joe Sr.', 'male')
print('joe parents_simple(): Mary, Joe Sr.'); print_people(joe.parents_simple())
joe.father.father = Person('Old Joe', 'male')
maternal_gm.mother = Person('Maternal ggm', 'female')
print('joe.grandparents(), Agnes, Old Joe'); print_people(joe.grandparents())
print('joe.grandparents_simple(), Agnes, Old Joe'); print_people(joe.grandparents_simple())
print('joe great-grandparents: Maternal ggm'); print_people(joe.ancestors(3))

# play with infinite limits
inf = float('inf')
print('joes ancestors: Mary, Joe Sr., Agnes, Old Joe, Maternal ggm'); print_people(joe.ancestors(1, inf))
print('joe and his ancestors'); print_people(joe.ancestors(0, inf))

joe.mother.add_child(joe)
print('joe.mother.sons():'); print_people(joe.mother.sons())
print('joe.sons()'); print_people(joe.mother.sons())
print('joe.sons():', joe.sons())
