""" Test transcribe and translate

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-11-28
"""

import unittest
import re
import copy

from trans_translator import TransTranslator


class TestTransTranslator(unittest.TestCase):

    def setUp(self):

        self.trans_translator = TransTranslator()

    def test_init(self):

        self.assertEqual(self.trans_translator.dna_rna, TransTranslator.DNA_RNA)
        self.assertEqual(self.trans_translator.rna_protein, TransTranslator.RNA_PROTEIN)
        self.assertEqual(self.trans_translator.start_codons, TransTranslator.START_CODONS)

        alternate_dna_rna = {'x': 'y'}
        alternate_rna_protein = {'x': 'y', 'a': 'b'}
        alternate_start_codons = {'x'}
        trans_translator = TransTranslator(dna_rna=alternate_dna_rna,
            rna_protein=alternate_rna_protein,
            start_codons=alternate_start_codons)
        self.assertEqual(trans_translator.dna_rna, alternate_dna_rna)
        self.assertEqual(trans_translator.rna_protein, alternate_rna_protein)
        self.assertEqual(trans_translator.start_codons, alternate_start_codons)

    def test_trans_trans(self):

        # DNA with 1 protein that's 1 AA long; no non-coding DNA
        chr = 'ATGGAATGA'
        self.assertEqual(self.trans_translator.trans_trans(chr), (['E'], 0, False))

        # DNA with 1 protein that's 1 AA long; trailing non-coding DNA; nucleotides not a multiple of 3
        chr = 'ATG CGT TAA CGT A'.replace(' ', '')
        self.assertEqual(self.trans_translator.trans_trans(chr), (['R'], 4, False))

        # DNA with no protein
        chr = 'ATTATTATT'
        self.assertEqual(self.trans_translator.trans_trans(chr), ([], len(chr), True))

        # DNA with a 0-length protein; no non-coding DNA
        chr = 'ATGTAA'
        self.assertEqual(self.trans_translator.trans_trans(chr), ([], 0, True))

        # DNA failure: ends while encoding a protein
        chr = 'ATGCGTCGT'
        self.assertEqual(self.trans_translator.trans_trans(chr), ([], 0, True))

        # test exceptions
        chr = 'ABD'
        with self.assertRaisesRegex(ValueError, re.escape("bad bases in ABD at positions [1, 2]")):
            self.trans_translator.trans_trans(chr)

        # RNA_PROTEIN covers all possible codons, so must delete one to generate the unknown codon error
        # copy TransTranslator.RNA_PROTEIN so that the one in TransTranslator does not get changed
        rna_protein_copy = copy.deepcopy(TransTranslator.RNA_PROTEIN)
        del rna_protein_copy['UCU']
        # use the rna_protein keyword argument to use the changed RNA_PROTEIN dict
        trans_translator = TransTranslator(rna_protein=rna_protein_copy)
        chr = 'ATGTCTTGA'
        with self.assertRaisesRegex(ValueError, "unknown codon 'UCU' at pos 3 in AUGUCUUGA"):
            trans_translator.trans_trans(chr)

    def trans_trans_genome(self, genome):
        trans_translator = TransTranslator()
        trans_translator.trans_trans_genome(genome)
        return trans_translator

    def test_trans_trans_genome(self):
        genome = [
            'ABD',
            'ATTATTATT',
            'ATGGAATGA'
        ]
        trans_translator = self.trans_trans_genome(genome)
        self.assertEqual(trans_translator.proteins, [[], ['E']])
        self.assertEqual(trans_translator.num_noncoding_bases, len(genome[1]))
        self.assertEqual(trans_translator.num_DNA_failures, 1)

        genome = [
            'ATTATTATT',
            'ATGGAATGA'
        ]
        trans_translator = self.trans_trans_genome(genome)
        self.assertEqual(trans_translator.proteins, [[], ['E']])

    def test_genome_stats(self):
        genome = [
            'ATTATTATT',
            'ATGGAATGA'
        ]
        trans_translator = self.trans_trans_genome(genome)
        data = trans_translator.genome_stats()
        self.assertEqual(data['proteins'], [[], ['E']])
        self.assertEqual(data['number_proteins'][0], 2)
        self.assertEqual(data['len_shortest_protein'][0], 0)
        self.assertEqual(data['len_longest_protein'][0], 1)
        self.assertEqual(data['mean_protein_length'][0], 0.5)
        self.assertEqual(data['num_DNA_failures'][0], 1)
        self.assertEqual(data['total_noncoding_bases'][0], len(genome[1]))
