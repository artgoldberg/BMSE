""" OO version of solution to HW 3: Write a Python program, Biomedical Software Engineering, fall 2018

:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Author: Ryan Neff ryan.neff@icahn.mssm.edu
:Author: Nicole Zatorski nicole.zatorski@icahn.mssm.edu
:Date: 2018-10-10
"""

import sys
from numpy import mean


class TransTranslator(object):

    DNA_RNA = {"A": "A",
                "C": "C",
                "G": "G",
                "T": "U"}

    RNA_PROTEIN = {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
         'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
         'UAU': 'Y', 'UAC': 'Y', 'UAA': 'STOP', 'UAG': 'STOP',
         'UGU': 'C', 'UGC': 'C', 'UGA': 'STOP', 'UGG': 'W',
         'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
         'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
         'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
         'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
         'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
         'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
         'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
         'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
         'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
         'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
         'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
         'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'}

    START_CODONS = {"AUG"}

    CODON_LEN = 3

    def __init__(self, dna_rna=None, rna_protein=None, start_codons=None):
        """

        Args:
            dna_rna (:obj:`dict`, optional): table that translates DNA to RNA
            rna_protein (:obj:`dict`, optional): table that translates RNA codons to AAs, encoded
                by their single letter code, or 'STOP', indicating a stop codon
            start_codons (:obj:`set`, optional): start codon strings that initiate translation
        """

        self.dna_rna = self.DNA_RNA if dna_rna is None else dna_rna
        self.rna_protein = self.RNA_PROTEIN if rna_protein is None else rna_protein
        self.start_codons = self.START_CODONS if start_codons is None else start_codons
        self.chromosomes = []
        self.proteins = []
        self.num_noncoding_bases = 0
        self.num_DNA_failures = 0

    def trans_trans(self, chromosome):
        """ Transcribe and translate a chromosome to protein(s), and provide a couple of its properties

        Simplified and biologically inaccurate -- transcribes all DNA to RNA, and then translates.

        Args:
            chromosome (:obj:`str`): an input sequence of A, C, T or G, all uppercase

        Returns:
            :obj:`tuple`: list of proteins encoded, number of non-coding bases, whether DNA failure occurred

        Raises:
            :obj:`ValueError`: if `chromosome` contains bad bases or unknown codons
        """

        # validate chromosome
        bad_base_positions = []
        good_bases = set(self.dna_rna)
        for idx, base in enumerate(chromosome):
            if not base in good_bases:
                bad_base_positions.append(idx)
        if bad_base_positions:
            raise ValueError("bad bases in {} at positions {}".format(chromosome, bad_base_positions))

        # initialize chromosome properties
        proteins = []
        num_noncoding_bases = 0
        DNA_failure = False

        # translate DNA to RNA
        rna_chromosome = ''.join([self.dna_rna[base] for base in chromosome])

        # transcribe and translate
        # use a state machine that transitions between translating and not translating
        translating = False
        for codon_start_pos in range(0, len(rna_chromosome), self.CODON_LEN):
            codon = rna_chromosome[codon_start_pos:codon_start_pos + self.CODON_LEN]
            if len(codon) != self.CODON_LEN:
                # at end of chromosome, and number of bases in chromosome isn't a multiple of CODON_LEN
                num_noncoding_bases += len(codon)
                break
            if not translating:
                if codon in self.start_codons:
                    # the codon is AUG
                    translating = True
                    # record a protein as a list of AAs
                    protein = []
                    continue
                else:
                    num_noncoding_bases += self.CODON_LEN
            else:
                # raise exception if the codon can't be translated
                if codon not in self.rna_protein:
                    raise ValueError("unknown codon '{}' at pos {} in {}".format(codon, codon_start_pos,
                        rna_chromosome))
                translated_codon = self.rna_protein[codon]
                if translated_codon == "STOP":
                    translating = False
                    if protein:
                        proteins.append(''.join(protein))
                    continue
                amino_acid = translated_codon
                protein.append(amino_acid)

        # DNA failure if still translating at end of chromosome or no proteins found
        if translating or not proteins:
            DNA_failure = True

        return (proteins, num_noncoding_bases, DNA_failure)

    def trans_trans_genome(self, genome):
        """ Transcribe and translate a genome

        Args:
            genome (:obj:`list`): the chromosomes in a genome
        """

        errors = []
        for chromosome in genome:
            self.chromosomes.append(chromosome)
            try:
                proteins, num_NC_bases, DNA_failure = self.trans_trans(chromosome)
                self.proteins.append(proteins)
                self.num_noncoding_bases += num_NC_bases
                self.num_DNA_failures += 1 if DNA_failure else 0
            except ValueError as e:
                errors.append(str(e))
        if errors:
            print('\n'.join(errors), file=sys.stderr)

    def genome_stats(self):
        """ Report a genome's stats

        Returns:
            :obj:`dict`: dict of stats, pairs of value, units
        """

        len_shortest = min([len(p) for p in self.proteins]) if self.proteins else float('NaN')
        len_longest = max([len(p) for p in self.proteins]) if self.proteins else float('NaN')
        mean_len = mean([len(p) for p in self.proteins]) if self.proteins else float('NaN')

        data = {
            "proteins": self.proteins,
            "number_proteins": (len(self.proteins), "proteins"),
            "len_shortest_protein": (len_shortest, "amino acids"),
            "len_longest_protein": (len_longest, "amino acids"),
            "mean_protein_length": (mean_len, "amino acids"),
            "num_DNA_failures": (self.num_DNA_failures, "dimensionless"),
            "total_noncoding_bases": (self.num_noncoding_bases, "bases")
            }

        return data
