""" Test RelatedPerson

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
:Copyright: 2017-2018, Arthur Goldberg
:License: MIT
"""
import unittest

from related_person import RelatedPerson, Gender, RelatedPersonError


class TestGender(unittest.TestCase):

    def test_gender(self):
        self.assertEqual(Gender().get_gender('Male'), Gender.MALE)
        self.assertEqual(Gender().get_gender('NA'), Gender.UNKNOWN)

        with self.assertRaises(RelatedPersonError) as context:
            Gender().get_gender('---')
        self.assertRegex(Gender().genders_string_mappings(), "'f'.* -> 'F'")

class TestRelatedPerson(unittest.TestCase):

    def setUp(self):
        # create a few RelatedPersons
        self.child = RelatedPerson('kid', 'NA')
        self.mom = RelatedPerson('mom', 'f')
        self.dad = RelatedPerson('dad', 'm')

        # make a deep family history
        self.generations = 6
        self.people = people = []
        self.root_child = RelatedPerson('root_child', Gender.UNKNOWN)
        people.append(self.root_child)

        def add_parents(child, depth, max_depth):
            if depth+1 < max_depth:
                dad = RelatedPerson(child.name + '_dad', Gender.MALE)
                mom = RelatedPerson(child.name + '_mom', Gender.FEMALE)
                people.append(dad)
                people.append(mom)
                child.set_father(dad)
                child.set_mother(mom)
                add_parents(dad, depth+1, max_depth)
                add_parents(mom, depth+1, max_depth)
        add_parents(self.root_child, 0, self.generations)

    def test_add_child_error(self):
        self.dad.gender = Gender.UNKNOWN
        with self.assertRaises(RelatedPersonError) as context:
            self.dad.add_child(self.child)
        self.assertRegex(str(context.exception), "cannot add child.*with unknown gender")

    def test_remove_father(self):
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotIn(self.child, self.dad.children)

    def test_ancestors_error(self):
        with self.assertRaises(RelatedPersonError) as context:
            self.root_child.ancestors(3, 2)
        self.assertRegex(str(context.exception), "max_depth.*cannot be less than min_depth")

    def test_parents(self):
        pass

    def test_all_grandparents(self):
        all_grandparents = set(self.people).difference([self.root_child], self.root_child.parents())
        self.assertEqual(self.root_child.all_grandparents(), all_grandparents)

    def test_all_ancestors(self):
        self.assertEqual(self.root_child.all_ancestors(), set(self.people[1:]))
