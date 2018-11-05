""" Subjects, and reading them from files

Supported file type:

* Tab separated values (.tsv)

:Author: Nicole Zatorski <nicole.zatorski@icahn.mssm.edu>
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-11-01
:Copyright: 2018, Arthur Goldberg
"""

from enum import Enum
import sys
import csv
from datetime import datetime


class Gender(Enum):
    """ Gender categories """
    female = 1
    male = 2
    unknown = 3


class XStatus(Enum):
    """ Status categories for condition X """
    unaffected = 1
    affected = 2


class Subject:
    """ Read, verify and store information about a submect

    Attributes:
        id (:obj:`str`): a unique identifier for each `Subject`
        gender (:obj:`Gender`): a `Subject`'s gender; may be unknown
        dob (:obj:`Date`): date of birth
        x_status (:obj:`str`): a `Subject`'s status on condition X
    """
    # TODO(BMSE student) replace NUM_ATTRIBUTES with a list of expected column headers so that load_instance() can
    # check that column headers in row are correct
    NUM_ATTRIBUTES = 4
    MIN_ID_LEN = 4

    def __init__(self, id, gender, dob, x_status):
        self.id = id
        self.gender = Gender[gender]
        date = datetime.strptime(dob, '%Y-%m-%d').date()
        self.dob = date
        self.x_status = XStatus[x_status]

    @classmethod
    def verify(cls, id, gender, dob, x_status):
        """ Verify the attributes of a `Subject` instance

        Args:
            id (:obj:`str`): a unique identifier for each `Subject`
            gender (:obj:`Gender`): a `Subject`'s gender; may be unknown
            dob (:obj:`Date`): date of birth
            x_status (:obj:`str`): a `Subject`'s status on condition X

        Returns:
            :obj:`list`: detected errors; empty list if none
        """
        errors = []
        if not isinstance(id, str):
            errors.append("id '{}' is not a str".format(id))
        elif len(id) < cls.MIN_ID_LEN:
            errors.append("id '{}' is shorter than min {}".format(id, cls.MIN_ID_LEN))
        # TODO(BMSE student) use RE to ensure that ids dont contain white-space
        try:
            Gender[gender]
        except KeyError:
            errors.append("gender '{}' is not a Gender name".format(gender))
        try:
            # check that dob is in 'YYYY-MM-DD' format
            datetime.strptime(dob, '%Y-%m-%d')
            # TODO(BMSE student) check that Date of birth occurs in the last 150 years
        except Exception as e:
            errors.append("dob '{}' error {}".format(dob, e))
        try:
            XStatus[x_status]
        except KeyError:
            errors.append("x_status '{}' is not an XStatus name".format(x_status))
        return errors

    def __str__(self):
        """ Provide string repr

        Returns:
            :obj:`str`: tab-separated id, gender, dob, and status
        """
        return '\t'.join([self.id, self.gender.name, str(self.dob), self.x_status.name])

    @classmethod
    def load_instance(cls, row):
        """ Instantiate a `Subject` instance from `row` or report errors in it

        Args:
            row (:obj:`OrderedDict`): values in the row, keyed by header values; see csv docs for
                more info
        """
        # TODO(BMSE student) check that column headers in row are correct
        if len(row.keys()) != cls.NUM_ATTRIBUTES:
            # TODO(BMSE student) provide info in error
            return 'error'
        # TODO(BMSE student) check for data in extra fields

        # check for errors in fields
        # this uses the *args construct, which is very handy for passing a list in a function call
        # see https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists
        # and https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
        args = list(row.values())
        error = Subject.verify(*args)
        if error:
            return error

        subject = Subject(*args)
        return subject

    @classmethod
    def load_file(cls, file_name):
        # TODO(BMSE student) add doc string
        subjects = []
        errors = []
        # start with row num 2 because DictReader uses headers as keys
        row_num = 2
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t', restkey='extra_fields')
            for row in reader:
                return_value = cls.load_instance(row)
                if isinstance(return_value, Subject):
                    subjects.append(return_value)
                else:
                    errors.append("{}:{} {}".format(file_name, row_num, '; '.join(return_value)))
                row_num += 1
        if errors:
            sys.stderr.write('\n'.join(errors))
            sys.stderr.write('\n')
        # TODO(BMSE student) check that all subjects all have unique ids
        return subjects

# TODO(BMSE student) move this code to a separate test_subjects.py module
good_data = ['18795', 'female', '2005-01-07', 'affected']
assert not Subject.verify(*good_data)
bad_val_lists = [[18, 'Judy', '005-01-07', 'not affected'], ['hi', None, None, None]]
for bad_vals in bad_val_lists:
    for idx, val in enumerate(bad_vals):
        if val is not None:
            args = good_data.copy()
            args[idx] = val
            assert Subject.verify(*args), 'error not found'
