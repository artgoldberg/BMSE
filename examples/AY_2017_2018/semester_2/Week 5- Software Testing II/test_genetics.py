"""
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-01-30
:Copyright: 2018, Arthur Goldberg
"""
import unittest

from genetics import Genetics

class TestGenetics(unittest.TestCase):

    def test_count_dna_ntides(self):
        one_of_each_genome = 'TACG'
        genetics = Genetics(one_of_each_genome)
        counts = genetics.count_dna_ntides()
        for ntide in Genetics.DNA_NUCLEOTIDES:
            self.assertEqual(counts[ntide], 1)

        genetics = Genetics('')
        counts = genetics.count_dna_ntides()
        for ntide in Genetics.DNA_NUCLEOTIDES:
            self.assertEqual(counts[ntide], 0)

    def test_check_genome(self):
        good_genome = 'AAACTGGGGNN'
        try:
            Genetics.check_genome(good_genome)
        except ValueError:  # pragma: no cover
            self.fail("check_genome should not raise an exception")

        bad_genome = "ARTHURS NECK"
        with self.assertRaises(ValueError) as context:
            Genetics.check_genome(bad_genome)
        self.assertRegex(str(context.exception),
            "the genome .* contains illegal character codes")

if __name__ == '__main__':
    unittest.main()
