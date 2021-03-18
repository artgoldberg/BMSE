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

    def test_fasta_reader(self):
      fasta_with_var_num_lines = os.path.join(self.good_fasta_files,
                                              'fasta_with_various_num_lines_for_mini_chromo.fna')
      self.assertTrue(isinstance(FastaReader(fasta_with_var_num_lines), FastaReader))
      chromos = FastaReader(fasta_with_var_num_lines).read()
      self.assertEqual(chromos, ['ATG', 'ATG'*2, 'ATG'*8])

      mini_chromo_shared_with_hw5 = os.path.join(self.good_fasta_files,
                                                 'mini_chromo_shared_with_HW5.fna')
      chromos = FastaReader(mini_chromo_shared_with_hw5).read()
      self.assertEqual(len(chromos), 3)

    def test_fasta_reader_errors(self):
      with self.assertRaisesRegex(ValueError, "FASTA pathname isn't a string: "):
        FastaReader(1)

      with self.assertRaisesRegex(ValueError, "FASTA pathname isn't a file"):
        FastaReader('no such file')

      fasta_with_non_fasta_extension = os.path.join(self.bad_fasta_files,
                                                    'illegal_fasta_with_non_fasta_extension.txt')
      with self.assertRaisesRegex(ValueError, "pathname '.*' doesn't have a FASTA suffix"):
        FastaReader(fasta_with_non_fasta_extension)
