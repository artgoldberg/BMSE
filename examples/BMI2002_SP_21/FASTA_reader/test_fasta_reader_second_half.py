""" Test FastaReader

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2021-03-13
"""

import os
import unittest

from fasta_reader_w_bugs import FastaReader


class TestFastaReader(unittest.TestCase):

    def setUp(self):
        self.fixtures = os.path.join(os.path.dirname(__file__), '..', 'assignment_5', 'tests',
                                    'fixtures')
        self.good_fasta_files = os.path.join(self.fixtures, 'good_fasta_files')
        self.bad_fasta_files = os.path.join(self.fixtures, 'bad_fasta_files')

    def test_fasta_reader_errors(self):
      illegal_fasta_unreadable = os.path.join(self.bad_fasta_files, 'illegal_fasta_unreadable.fna')
      with self.assertRaisesRegex(PermissionError, "Cannot read FASTA file: '.+'"):
        FastaReader(illegal_fasta_unreadable).read()

      fasta_with_no_description_line = os.path.join(self.bad_fasta_files,
                                                    'illegal_fasta_with_no_description_line.fna')
      with self.assertRaisesRegex(ValueError, "missing description line that starts with '>'"):
        FastaReader(fasta_with_no_description_line).read()

      fasta_with_empty_sequence = os.path.join(self.bad_fasta_files,
                                               'illegal_fasta_with_empty_sequence.fna')
      with self.assertRaisesRegex(ValueError, ".*: empty sequence"):
        FastaReader(fasta_with_empty_sequence).read()

      fasta_with_empty_line_in_seq = os.path.join(self.bad_fasta_files,
                                                  'illegal_fasta_with_empty_line_in_sequence.fna')
      with self.assertRaisesRegex(ValueError, ".*: empty line"):
        FastaReader(fasta_with_empty_line_in_seq).read()

      fasta_with_illegal_chars = os.path.join(self.bad_fasta_files,
                                              'illegal_fasta_with_chars_not_nucleotides.fna')
      with self.assertRaisesRegex(ValueError, ".+: invalid nucleotides .+"):
        FastaReader(fasta_with_illegal_chars).read()
