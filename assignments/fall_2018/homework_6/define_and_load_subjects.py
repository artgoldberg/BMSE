import pandas
from enum import Enum

class Gender(Enum):
	F = 1
	M = 2

class XStatus(Enum):
	unaffected = 1
	affected = 2

class Subject:
	# initializes a Subject with ID (int), gender (str), date of birth (YYYY-MM-DD), and x status (str affected, unaffected)
	def __init__(self, ID, gender, dob, x_status):
		self.ID = ID
		self.gender = gender
		self.dob = dob
		self.x_status = x_status

	# getter methods for all of a Subject's attributes
	def get_ID(self):
		return self.ID

	def get_gender(self):
		return self.gender

	def get_dob(self):
		return self.dob

	def get_x_status(self):
		return self.x_status

    @staticmethod
    def load_file(file_name):
        # todo: doc string
        subjects = []
        # todo: catch exceptions
        data = pandas.read_table(file_name, sep='\t', lineterminator ='\r')
        for row in range(1, len(data)):
            subject_entry = data.iloc[row,:]
            # todo: error checking
            subjects.append(Subject(subject_entry[0],
                Gender[subject_entry[1]], subject_entry[2], XStatus[subject_entry[3]]))
        return subjects
