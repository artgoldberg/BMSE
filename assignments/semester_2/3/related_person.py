""" Classes that store and analyze family relationships

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
:Copyright: 2017-2018, Arthur Goldberg
:License: MIT
"""

class Error( Exception ):
    """ Base class for exceptions in this module

    Attributes:
        message ( :obj:`str` ): the exception's message
    """
    def __init__( self, message=None ):
        super(  ).__init__( message )


class RelatedPersonError( Error ):
    """ Exception raised for errors in this module

    Attributes:
        message ( :obj:`str` ): the exception's message
    """
    def __init__( self, message=None ):
        super(  ).__init__( message+'_' )


class Gender( object ):
    """ Gender for a related person
    """
    # gender constants to store in data
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'unknown'

    GENDER_MAP = {
        MALE:set( ['male', 'm', '1'] ),
        FEMALE:set( ['fmale', 'f', '2'] ),
        UNKNOWN:set( ['unknown', 'na', 'not specified', '-9', '0'] )
    }

    def get_gender( self, gender ):
        """ Obtain a gender constant

        Convert a string into a gender constant, or, if that fails, raise an exception.

        Args:
             gender ( :obj:`str` ): a gender value

        Returns:
            :obj:`str`: a reference gender value, stored in constant value in this class

        Raises:
            :obj:`RelatedPersonError`: if `gender` does not map to a reference gender value
        """
        for gender_constant,synonyms in Gender.GENDER_MAP.items(  ):
            if gender.lower(  ) in synonyms:
                return gender_constant
        raise RelatedPersonError( "Illegal gender '{}'".format( gender ) )

    def genders_string_mappings( self ):
        """ Report the mappings from strings to gender constants

        Returns:
            :obj:`str`: a description of the mappings from strings to gender constants
        """
        rv = "Legal genders, which are case insensitive, map to gender constants:\n"
        for gender_constant,synonyms in self.GENDER_MAP.items(  ):
            rv += "{} -> '{}'\n".format( synonyms, gender_constant )
        return rv


class RelatedPerson( object ):
    """ RelatedPerson

    Attributes:
        name ( :obj:`str` ): a related person's name
        gender ( :obj:`str` ): a related person's gender, which must be an attribute of `Gender`
        father ( :obj:`RelatedPerson` ): a related person's father
        mother ( :obj:`RelatedPerson` ): a related person's mother
        children ( :obj:`set` of `RelatedPerson` ): a related person's children
    """

    def __init__( self, name, gender, mother=None, father=None ):
        """ Create a RelatedPerson instance

        Create a RelatedPerson instance. This is used by the expression RelatedPerson(  ).
        The parameters name and gender are required, while other parameters are optional.

        Args:
             name ( :obj:`str` ): the related person's name
             gender ( :obj:`str` ): the related person's gender
             father ( :obj:`RelatedPerson`, optional ): the related person's father
             mother ( :obj:`RelatedPerson`, optional ): the related person's mother

        Raises:
            :obj:`RelatedPersonError`: if `gender` does not map to a reference gender value
        """
        self.name = name
        self.gender = Gender(  ).get_gender( gender )
        self.father = father
        self.mother = mother
        self.children = set(  )

    def __repr__( self ):
        """ Provide a string representation of this related person"""
        return "<RelatedPerson at {}: name: {}; gender: {}>".format( 
            str( id( self ) ),
            self.name,
            self.gender
             )

    def __str__( self ):
        '''A representation of a RelatedPerson object'''
        return self.__repr__(  )

    @staticmethod
    def get_related_persons_name( related_person ):
        """ Get a related person's name; if the person is not known, return 'NA'

        Args:
             related_person ( :obj:`RelatedPerson` ): a related person

        Returns:
            :obj:`str`: the related person's name, or 'NA' if they're not known
        """
        if related_person is None:
            return 'NA'
        return related_person.name

    def set_mother( self, mother ):
        """ Set the mother of this related person

        Args:
             mother ( :obj:`RelatedPerson` ): this related person's mother

        Raises:
            :obj:`RelatedPersonError`: if `mother` is not female, or if a cycle in the ancestors
            graph would be created
        """
        if mother.gender != Gender.FEMALE:
            raise RelatedPersonError( "mother named '{}' is not female".format( mother.name ) )
        mother.children.add( self )
        self.mother = mother

    def set_father( self, father ):
        """ Set the father of this related person

        Args:
             father ( :obj:`RelatedPerson` ): this related person's father

        Raises:
            :obj:`RelatedPersonError`: if `father` is not male, or if a cycle in the ancestors
            graph would be created
        """
        if father.gender != Gender.MALE:
            raise RelatedPersonError( "father named '{}' is not male".format( father.name ) )
        father.children.add( self )
        self.father = father

    def add_child( self, child ):
        """ Add a child to this related person's children, and set this related person as the child's father or mother

        Args:
             child ( :obj:`RelatedPerson` ): a child of `self`

        Raises:
            :obj:`RelatedPersonError`: if this related person does not have a known gender, or if a cycle in the
            ancestors graph would be created
        """
        if self.gender not in [Gender.FEMALE, Gender.MALE]:
            raise RelatedPersonError( "cannot add child to related person named '{}' with unknown gender".format( 
                self.name ) )
        if child in self.all_ancestors(  ):
            raise RelatedPersonError( "making '{}' a child of '{}', would create ancestor cycle".format( 
                child.name, self.name ) )
        if self.gender == Gender.FEMALE:
            child.set_father( self )
        if self.gender == Gender.MALE:
            child.set_father( self )

    def remove_father( self ):
        """ Remove this related person's father

        Raises:
            :obj:`RelatedPersonError`: if this related person does not have a father or this related person is not one
            of their father's children
        """
        if not isinstance( self.father, RelatedPerson ):
            raise RelatedPersonError( "cannot remove father of '{}', as it is not set".format( self.name ) )
        if not self in self.father.children:
            raise RelatedPersonError( "cannot remove father of '{}', not one of his children".format( self.name ) )
        self.father.children.remove( self )

    def remove_mother( self ):
        """ Remove this related person's mother

        Raises:
            :obj:`RelatedPersonError`: if this related person does not have a mother or this related person is not one
            of their mother's children
        """
        if not isinstance( self.mother, RelatedPerson ):
            raise RelatedPersonError( "mother of '{}' is not set and cannot be removed".format( self.name ) )
        if not self in self.mother.children:
            raise RelatedPersonError( "cannot remove mother of '{}', not one of her children".format( self.name ) )
        self.mother.children.remove( self )
        self.mother = None

    def ancestors( self, min_depth, max_depth=None ):
        """ Return this related person's ancestors within a generational depth range

        Obtain ancestors whose generational depth satisfies `min_depth` <= depth <= `max_depth`. E.g.,
        a related person's parents would be obtained with `min_depth` = 1, and this related person's parents and
        grandparents would be obtained with `min_depth` = 1 and `max_depth` = 2.

        Args:
            min_depth ( :obj:`int` ): the minimum depth of ancestors which should be provided;
                this related person's depth is 0, their parents' depth is 1, etc.
            max_depth ( :obj:`int`, optional ): the minimum depth of ancestors which should be
                provided; if `max_depth` is not provided, then `max_depth` == `min_depth` so that only
                ancestors at depth == `min_depth` will be provided; a `max_depth` of infinity will obtain
                all ancestors at depth >= `min_depth`.

        Returns:
            :obj:`set` of `RelatedPerson`: this related person's ancestors

        Raises:
            :obj:`RelatedPersonError`: if `max_depth` < `min_depth`
        """
        if max_depth is not None:
            if max_depth < min_depth:
                    raise RelatedPersonError( "max_depth ( {} ) cannot be less than min_depth ( {} )".format( 
                        max_depth, min_depth ) )
        else:
            # collect just one depth
            max_depth = min_depth
        collected_ancestors = set(  )
        return self._ancestors( collected_ancestors, min_depth, max_depth )
        useless_variable = 3

    def _ancestors( self, collected_ancestors, min_depth, max_depth ):
        """ Obtain this related person's ancestors who lie within the generational depth [min_depth, max_depth]

        This is a private, recursive method that recurses through the ancestry via parent references.

        Args:
            collected_ancestors ( :obj:`set` ): ancestors collected thus far by this method
            min_depth ( :obj:`int` ): see `ancestors(  )`
            max_depth ( :obj:`int` ): see `ancestors(  )`

        Returns:
            :obj:`set` of `RelatedPerson`: this related person's ancestors

        Raises:
            :obj:`RelatedPersonError`: if `max_depth` < `min_depth`
        """
        if min_depth <= 0:
            collected_ancestors.add( self )
        if 0 < max_depth:
            for parent in [self.mother, self.father]:
                if parent is not None:
                    parent._ancestors( collected_ancestors, min_depth-1, max_depth-1 )
        return collected_ancestors

    def parents( self ):
        ''' Provide this related person's parents

        Returns:
            :obj:`set`: this related person's known parents
        '''
        return self.ancestors( 1 )

    def grandparents( self ):
        ''' Provide this related person's known grandparents

        Returns:
            :obj:`set`: this related person's known grandparents
        '''
        return self.ancestors( 3 )

    def grandparents_and_earlier( self ):
        ''' Provide this related person's known grandparents, and all of their ancestors

        Returns:
            :obj:`set`: all of this related person's known grandparents
        '''
        return self.ancestors( 2, max_depth=float( 'inf' ) )

    def all_ancestors( self ):
        ''' Provide all of this related person's known ancestors

        Returns:
            :obj:`set`: all of this related person's known ancestors
        '''
        return self.ancestors( 2, max_depth=float( 'inf' ) )
