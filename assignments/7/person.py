""" Person, with heredity and other characteristics

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
:Copyright: 2017, Arthur Goldberg
:License: MIT
"""

class Error(Exception):
    """ Base class for exceptions in this module
    """
    pass


class PersonError(Error):
    """ Exception raised for errors in this module

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class Gender(object):
    """ Gender for a person
    """
    # TODO: incorporate other genders
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'unknown'

    def __init__(self):
        # '1' and '2' map to male and female in PED files: see http://zzz.bwh.harvard.edu/plink/data.shtml#ped
        self.gender_map = {
            self.MALE:set(['male', 'm', '1']),
            self.FEMALE:set(['female', 'f', '2']),
            self.UNKNOWN:set(['unknown', 'na', 'not specified'])
        }

    def get_gender(self, gender):
        """ Obtain a gender constant

        Convert a string into a gender constant, or, if that fails, raise an exception.

        Args:
             gender (:obj:`str`): a gender value

        Returns:
            :obj:`str`: a reference gender value, stored in constant value in this class

        Raises:
            :obj:`PersonError`: if `gender` does not map to a reference gender value
        """
        for gender_constant,synonyms in self.gender_map.items():
            if gender.lower() in synonyms:
                return gender_constant
        raise PersonError("Illegal gender '{}'".format(gender))

    def genders_string_mappings(self):
        """ Report the mappings from strings to gender constants

        Returns:
            :obj:`str`: a description of the mappings from strings to gender constants
        """
        rv = "Legal genders, which are case insensitive, map to gender constants:\n"
        for gender_constant,synonyms in self.gender_map.items():
            rv += "{} -> {}\n".format(synonyms, gender_constant)
        return rv


class Person(object):
    """ Person

    Attributes:
        name (:obj:`str`): a person's name
        gender (:obj:`str`): a person's gender, which must be an attribute of `Gender`
        mother (:obj:`Person`): a person's mother
        father (:obj:`Person`): a person's father
        children (:obj:`set` of `Person`): a person's children
    """

    def __init__(self, name, gender, mother=None, father=None):
        """ Create a Person instance

        Create a Person instance. This is used by the expression Person().
        The parameters name and gender are required, while other parameters are optional.

        Args:
             name (:obj:`str`): the person's name
             gender (:obj:`str`): the person's gender
             mother (:obj:`Person`, optional): the person's mother
             father (:obj:`Person`, optional): the person's father

        Raises:
            :obj:`PersonError`: if `gender` does not map to a reference gender value
        """
        self.name = name
        self.gender = Gender().get_gender(gender)
        self.mother = mother
        self.father = father
        self.children = set()

    @staticmethod
    def get_persons_name(person):
        """ Get a person's name; if the person is not known, return 'NA'

        Returns:
            :obj:`str`: the person's name, or 'NA' if they're not known
        """
        if person is None:
            return 'NA'
        return person.name

    def set_mother(self, mother):
        """ Set the mother of this person

        Args:
             mother (:obj:`Person`): this person's mother

        Raises:
            :obj:`PersonError`: if `mother` is not female
        """
        if mother.gender != Gender.FEMALE:
            raise PersonError("mother named '{}' is not female".format(mother.name))
        mother.children.add(self)
        self.mother = mother

    def __str__(self):
        """ Provide a string representation of this person
        """
        return "{}: gender {}; mother {}; father {}".format(
            self.name,
            self.gender,
            Person.get_persons_name(self.mother),
            Person.get_persons_name(self.father))

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
            :obj:`PersonError`: if `max_depth` < `min_depth`
        """
        if max_depth is not None:
            if max_depth < min_depth:
                    raise PersonError("max_depth ({}) cannot be less than min_depth ({})".format(
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
            :obj:`PersonError`: if `max_depth` < `min_depth`
        """
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
        return self.ancestors(0)

    def grandparents(self):
        ''' Provide this person's known grandparents, by using ancestors()

        Returns:
            :obj:`set`: this person's known grandparents
        '''
        return self.ancestors(2)

    def all_grandparents(self):
        ''' Provide all of this person's known grandparents, from their parents' parents on back 

        Returns:
            :obj:`set`: all of this person's known grandparents
        '''
        return self.ancestors(3, max_depth=float('inf'))

    def all_ancestors(self):
        ''' Provide all of this person's known ancestors

        Returns:
            :obj:`set`: all of this person's known ancestors
        '''
        return self.ancestors(1, max_depth=float('inf'))
