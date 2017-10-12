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

joe = Person('Joe', 'male')
print(joe)
assert joe.name == 'Joe'
