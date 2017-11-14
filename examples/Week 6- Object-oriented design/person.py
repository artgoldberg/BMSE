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
        gender (:obj:`str`): a person's gender
        mother (:obj:`Person`): a person's mother
        father (:obj:`Person`): a person's father
        children (:obj:`set` of `Person`): a person's children
    """
    # TODO: add a data structure containing this person's variants, and methods that add a variant,
    # and list all variants

    def __init__(self, name, gender, mother=None, father=None):
        """ Create a Person instance

        Create a new Person object, AKA a Person instance. This is used by the
        expression Person(). The parameters name and gender are required, while   other parameters are
        optional.

        Args:
             name (:obj:`str`): the person's name
             gender (:obj:`str`): the person's gender
             mother (:obj:`Person`, optional): the person's mother
             father (:obj:`Person`, optional): the person's father
        """
        # TODO: standardize the representations of gender, so that M, m, and male are valid inputs
        # for male, but only one standard stored constant represents male, and similarly for female.
        self.name = name
        self.gender = gender
        self.mother = mother
        self.father = father
        self.children = set()

    # a method annotated with '@staticmethod' is a 'static method' that does not receive an
    # implicit first argument. Rather, it is called C.m(), where the class C identifies the
    # class in which the method is defined.
    @staticmethod
    def get_persons_name(person):
        """ Get a person's name; if the person is not known, return 'NA'

        Returns:
            :obj:`str`: the person's name, or 'NA' if they're not known
        """
        if person is None:
            return 'NA'
        return person.name

    def add_child(self, child):
        """ Add a child to this person's set of children

        Args:
             child (:obj:`Person`): a child of `self`
        """
        self.children.add(child)

    # TODO: write 'set_father' and 'set_mother' methods that set a person's father or mother,
    # and adds the person to the father's or mother's children. Replace all statements below
    # that set a person's father or mother attribute with these methods.

    # TODO: remove the 'add_child' method and replace any statements that use it with a call to
    # 'set_father' or 'set_mother'

    # TODO: write 'remove_father' and 'remove_mother' methods that removes a person's father or mother,
    # and removes the person from the father's or mother's children. Test these methods.

    # TODO: create a 'siblings' method that returns a person's siblings, and write a 'half_siblings'
    # method that returns a person's half-siblings.

    def sons(self):
        """ Get this person's sons

        Returns:
            :obj:`list` of `Person`: the person's sons
        """
        sons = []
        for child in self.children:
            if child.gender == 'male':
                sons.append(child)
        return sons

    def __str__(self):
        """ Provide a string representation of this person
        """
        return "{}: gender {}; mother {}; father {}".format(
            self.name,
            self.gender,
            Person.get_persons_name(self.mother),
            Person.get_persons_name(self.father))

    def grandparents_structured(self):
        ''' Provide this person's grandparents

        Returns:
            :obj:`tuple`: the person's grandparents, in a 4-tuple:
            (maternal grandmother, maternal grandfather, paternal grandmother, paternal grandfather)
            Missing individuals are identified by None.
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

    # TODO: EXTRA CREDIT: implement this descendants method, which has analogous semantics to the
    # ancestors method below. The implementation may use a while loop or be recursive.
    def descendants(self, min_depth, max_depth=None):
        """ Return this person's descendants within a generational depth range

        Obtain descendants whose generational depth satisfies `min_depth` <= depth <= `max_depth`.
        E.g., this person's children would be obtained with `min_depth` = 1, and this person's
        grandchildren and great-grandchildren would be obtained with `min_depth` = 3 and
        `max_depth` = 3.

        Args:
            min_depth (:obj:`int`): the minimum depth of descendants which should be provided;
                this person's depth is 0, their children's depth is 1, etc.
            max_depth (:obj:`int`, optional): the minimum depth of descendants which should be
                provided; if `max_depth` is not provided, then `max_depth` == `min_depth` so that only
                descendants at depth == `min_depth` will be provided; a `max_depth` of infinity will
                obtain all descendants at depth >= `min_depth`.

        Returns:
            :obj:`set` of `Person`: this person's descendants

        Raises:
            :obj:`ValueError`: if `max_depth` < `min_depth`
        """
        pass

    def ancestors(self, min_depth, max_depth=None):
        """ Return this person's ancestors within a generational depth range

        Obtain ancestors whose generational depth satisfies `min_depth` <= depth <= `max_depth`. E.g.,
        a person's parents would be obtained with `min_depth` = 1, and this person's parents and
        grandparents would be obtained with `min_depth` = 1 and `max_depth` = 2.

        Args:
            min_depth (:obj:`int`): the minimum depth of ancestors which should be provided;
                this person's depth is 0, their parents' depth is 1, etc.
            max_depth (:obj:`int`, optional): the minimum depth of ancestors which should be
                provided; if `max_depth` is not provided, then `max_depth` == `min_depth` so that only
                ancestors at depth == `min_depth` will be provided; a `max_depth` of infinity will obtain
                all ancestors at depth >= `min_depth`.

        Returns:
            :obj:`set` of `Person`: this person's ancestors

        Raises:
            :obj:`ValueError`: if `max_depth` < `min_depth`
        """
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
        """ Obtain this person's ancestors who lie within the generational depth [min_depth, max_depth]

        This is a private, recursive method that recurses through the ancestry via parent references.

        Args:
            collected_ancestors (:obj:`set`): ancestors collected thus far by this method
            min_depth (:obj:`int`): see `ancestors()`
            max_depth (:obj:`int`): see `ancestors()`

        Returns:
            :obj:`set` of `Person`: this person's ancestors

        Raises:
            :obj:`ValueError`: if `max_depth` < `min_depth`
        """
        # TODO: EXTRA CREDIT: a cycle in the ancestry graph will create an infinite loop;
        # avoid this problem
        if min_depth <= 0:
            collected_ancestors.add(self)
        if 0 < max_depth:
            for parent in [self.mother, self.father]:
                if parent is not None:
                    parent._ancestors(collected_ancestors, min_depth-1, max_depth-1)
        return collected_ancestors

    def parents(self):
        ''' Provide this person's parents

        Returns:
            :obj:`set`: this person's known parents
        '''
        return self.ancestors(1)

    def grandparents(self):
        ''' Provide this person's known grandparents, by using ancestors()

        Returns:
            :obj:`set`: this person's known grandparents
        '''
        return self.ancestors(2)

    def great_grandparents(self):
        return self.ancestors(3)

    def all_grandparents(self):
        ''' Provide all of this person's known grandparents, from their parents' parents on back 

        Returns:
            :obj:`set`: all of this person's known grandparents
        '''
        return self.ancestors(2, max_depth=float('inf'))

    def all_ancestors(self):
        ''' Provide all of this person's known ancestors

        Returns:
            :obj:`set`: all of this person's known ancestors
        '''
        return self.ancestors(1, max_depth=float('inf'))

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
