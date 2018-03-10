""" Main program that loads related people from a file

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-02-21
:Copyright: 2018, Arthur Goldberg
:License: MIT
"""

import argparse
import sys

import related_person
from related_person import Gender, RelatedPerson, RelatedPersonError


class RawPersonRecord(object):
    FIELDS = 5
    def __init__(self, id, name, father_id, mother_id, gender, row):
        self.id = id
        self.name = name
        self.father_id = father_id
        self.mother_id = mother_id
        self.gender = gender
        self.row = row

    @staticmethod
    def make_from_line(line, row):
        l = line.strip().split('\t')
        if len(l) != RawPersonRecord.FIELDS:
            raise ValueError("row {}: has {} fields, not {}".format(row, len(l), RawPersonRecord.FIELDS))
        t = tuple(l+[row])
        return RawPersonRecord(*t)


class LoadPeople(object):
    NULL_ID = '0'

    def __init__(self):
        self.buffer = []
        self.people_index = {}

    @staticmethod
    def all_people(people_index):
        print()
        for id in sorted(people_index.keys()):
            print(str(people_index[id]))

    def phase1(self):
        parser = argparse.ArgumentParser(description="Load related people from a file")
        parser.add_argument('--log_file', '-l', type=str, help="File for logging data")
        parser.add_argument('-p', '--people_data', required=True, type=argparse.FileType('r'), 
            help="File with related people, tab delimited; can be provided on stdin")
        return parser.parse_args()

    def phase2(self, people_data):
        # Phase 2:
        row = 0
        errors = []
        bad_ids = set()
        for line in people_data:
            row += 1
            try:
                self.buffer.append(RawPersonRecord.make_from_line(line, row))
            except ValueError as e:
                errors.append(str(e))

        # check IDs, genders, & create RelatedPersons
        for raw_person in self.buffer:
            try:
                # check for dupes
                if raw_person.id in self.people_index:
                    bad_ids.add(raw_person.id)
                    del self.people_index[raw_person.id]
                if raw_person.id in bad_ids:
                    raise RelatedPersonError("duplicate ID: {}".format(raw_person.id))

                # get and check gender
                gender = Gender.get_gender(raw_person.gender)

                # make RelatedPerson
                related_person = RelatedPerson(raw_person.id, raw_person.name, gender)
                self.people_index[raw_person.id] = related_person
            except RelatedPersonError as e:
                errors.append("row {}: {}".format(raw_person.row, str(e)))

        if errors:
            sys.stderr.write('\n- individual errors -\n')
            sys.stderr.write('\n'.join(errors))
            sys.stderr.write('\n')

    def check_parent(self, raw_person, parent):
        if parent == 'mother':
            if raw_person.mother_id != LoadPeople.NULL_ID:
                if raw_person.mother_id not in self.people_index:
                    raise RelatedPersonError("{} missing mother {}".format(raw_person.id, raw_person.mother_id))
        elif parent == 'father':
            if raw_person.father_id != LoadPeople.NULL_ID:
                if raw_person.father_id not in self.people_index:
                    raise RelatedPersonError("{} missing father {}".format(raw_person.id, raw_person.father_id))

    def set_parent(self, raw_person, parent):
        related_person = self.people_index[raw_person.id]
        if parent == 'mother':
            if raw_person.mother_id != LoadPeople.NULL_ID:
                mother = self.people_index[raw_person.mother_id]
                related_person.set_mother(mother)
        elif parent == 'father':
            if raw_person.father_id != LoadPeople.NULL_ID:
                father = self.people_index[raw_person.father_id]
                related_person.set_father(father)

    def phase3(self):
        # Phase 3:
        errors = []
        bad_ids = set()
        
        for raw_person in self.buffer:
            if raw_person.id in self.people_index:

                # check existence of parents
                for parent in ['mother', 'father']:
                    try:
                        self.check_parent(raw_person, parent)
                    except RelatedPersonError as e:
                        errors.append("row {}: {}".format(raw_person.row, str(e)))
                        bad_ids.add(raw_person.id)

                # set parents, which checks their gender
                if raw_person.id not in bad_ids:
                    for parent in ['mother', 'father']:
                        try:
                            self.set_parent(raw_person, parent)
                        except RelatedPersonError as e:
                            errors.append("row {}: for {} {}".format(raw_person.row, raw_person.id, str(e)))
                            bad_ids.add(raw_person.id)

        # delete all the bad people
        for bad_id in bad_ids:
            del self.people_index[bad_id]
        
        if errors:
            sys.stderr.write('\n- relatedness errors -\n')
            sys.stderr.write('\n'.join(errors))
            sys.stderr.write('\n')

    def main(self):
        args = self.phase1()
        self.phase2(args.people_data)
        self.phase3()
        self.all_people(self.people_index)

LoadPeople().main()
