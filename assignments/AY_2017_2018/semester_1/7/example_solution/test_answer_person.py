""" Test Person

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
:Copyright: 2017, Arthur Goldberg
:License: MIT
"""
import unittest

from answer_person import Person, Gender, PersonError


class TestGender(unittest.TestCase):

    def test_gender(self):
        self.assertEqual(Gender().get_gender('Male'), Gender.MALE)
        self.assertEqual(Gender().get_gender('female'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('FEMALE'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('NA'), Gender.UNKNOWN)

        with self.assertRaises(PersonError) as context:
            Gender().get_gender('---')
        self.assertRegex(Gender().genders_string_mappings(), "'f'.* -> 'F'")


class TestPerson(unittest.TestCase):

    def setUp(self):
        # create a few Persons
        self.child = Person('kid', 'NA')
        self.mom = Person('mom', 'f')
        self.dad = Person('dad', 'm')

        # make a deep family history
        self.generations = 4
        self.people = people = []
        self.root_child = Person('root_child', Gender.UNKNOWN)
        people.append(self.root_child)

        def add_parents(child, depth, max_depth):
            if depth+1 < max_depth:
                dad = Person(child.name + '_dad', Gender.MALE)
                mom = Person(child.name + '_mom', Gender.FEMALE)
                people.append(dad)
                people.append(mom)
                child.set_father(dad)
                child.set_mother(mom)
                add_parents(dad, depth+1, max_depth)
                add_parents(mom, depth+1, max_depth)
        add_parents(self.root_child, 0, self.generations)

    def test_get_persons_name(self):
        self.assertEqual(Person.get_persons_name(self.child), 'kid')
        self.assertEqual(Person.get_persons_name(None), 'NA')

    def test_set_mother(self):
        self.child.set_mother(self.mom)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)

        self.mom.gender = Gender.MALE
        with self.assertRaises(PersonError) as context:
            self.child.set_mother(self.mom)
        self.assertIn('is not female', str(context.exception))

    def test_set_father(self):
        self.child.set_father(self.dad)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)

        self.dad.gender = Gender.UNKNOWN
        with self.assertRaises(PersonError) as context:
            self.child.set_father(self.dad)
        self.assertIn('is not male', str(context.exception))

    def test_add_child(self):
        self.assertNotIn(self.child, self.mom.children)
        self.mom.add_child(self.child)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)

        self.assertNotIn(self.child, self.dad.children)
        self.dad.add_child(self.child)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)

    def test_add_child_error(self):
        self.dad.gender = Gender.UNKNOWN
        with self.assertRaises(PersonError) as context:
            self.dad.add_child(self.child)
        self.assertRegex(str(context.exception), "cannot add child.*with unknown gender")

        # attempt to make an ancestor cycle
        self.root_child.gender = Gender().get_gender('f')
        with self.assertRaises(PersonError) as context:
            self.root_child.add_child(self.people[-1])
        self.assertRegex(str(context.exception), "making.*a child of.*, would create ancestor cycle")

    def test_remove_father(self):
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotIn(self.child, self.dad.children)

    def test_remove_father_error1(self):
        self.dad.add_child(self.child)
        self.child.father = None
        with self.assertRaises(PersonError) as context:
            self.child.remove_father()
        self.assertRegex(str(context.exception), "cannot remove father of '.*', as it is not set")

    def test_remove_father_error2(self):
        self.dad.add_child(self.child)
        self.dad.children = set()
        with self.assertRaises(PersonError) as context:
            self.child.remove_father()
        self.assertRegex(str(context.exception), "cannot remove father of.*not one of his children")

    def test_remove_mother(self):
        self.child.set_mother(self.mom)
        self.child.remove_mother()
        self.assertNotIn(self.child, self.mom.children)

    def test_remove_mother_error1(self):
        self.mom.add_child(self.child)
        self.child.mother = None
        with self.assertRaises(PersonError) as context:
            self.child.remove_mother()
        self.assertRegex(str(context.exception), "mother of.*is not set and cannot be removed")

    def test_remove_mother_error2(self):
        self.mom.add_child(self.child)
        self.mom.children = set()
        with self.assertRaises(PersonError) as context:
            self.child.remove_mother()
        self.assertRegex(str(context.exception), "cannot remove mother of.*not one of her children")

    def test_ancestors_error(self):
        with self.assertRaises(PersonError) as context:
            self.root_child.ancestors(3, 2)
        self.assertRegex(str(context.exception), "max_depth.*cannot be less than min_depth")

    def test_parents(self):
        self.assertIn(self.root_child.mother, self.root_child.parents())
        self.assertIn(self.root_child.father, self.root_child.parents())
        self.assertEqual(2, len(self.root_child.parents()))

    def test_grandparents(self):
        self.assertEqual(self.root_child.grandparents(), set([
                self.root_child.mother.mother,
                self.root_child.mother.father,
                self.root_child.father.mother,
                self.root_child.father.father]))

    def test_all_grandparents(self):
        all_grandparents = set(self.people).difference([self.root_child], self.root_child.parents())
        self.assertEqual(self.root_child.all_grandparents(), all_grandparents)

    def test_all_ancestors(self):
        self.assertEqual(self.root_child.all_ancestors(), set(self.people[1:]))

if __name__ == '__main__':
    unittest.main()