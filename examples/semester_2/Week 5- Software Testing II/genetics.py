"""
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-01-30
:Copyright: 2018, Arthur Goldberg
"""

class Genetics(object):
    """ Store and analyze a genome
    """

    DNA_NUCLEOTIDES = ['A', 'C', 'G', 'T']
    # This list is NOT complete:
    NON_SPECIFIC_DNA_NUCLEOTIDES = \
        ['N',   # Unidentified nucleic acid
        '-']    # gap of indeterminate length

    def __init__(self, genome):
        """ Create a Genetics instance
        """
        self.check_genome(genome)
        self.genome = genome

    def count_dna_ntides(self):
        """ Count the DNA nucleotides

        Returns:
            :obj:`dict`: map from DNA nucleotide to its count in the genome
        """
        counts = {}
        for ntide in Genetics.DNA_NUCLEOTIDES:
            counts[ntide] = self.genome.count(ntide)
        return counts

    @staticmethod
    def check_genome(genome):
        """ Check a genome

        Args:
            genome (:obj:`str`): a genome, as a string of DNA nucleotides

        Raises:
            :obj:`ValueError`: if `genome` contains illegal character codes
        """
        legal_codes = set(Genetics.DNA_NUCLEOTIDES + Genetics.NON_SPECIFIC_DNA_NUCLEOTIDES)
        if not legal_codes.issuperset(genome):
            raise ValueError("the genome '{}' contains illegal character codes: '{}'".format(
                genome, set(genome) - legal_codes))
