class MiniChromosome(object):

    def __init__(self, mini_chromosome):
        self.mini_chromosome = mini_chromosome

    def find_orfs(self):
        """ find the ORFs for this mini-chromosome """
        # sets of START and STOP codons (could derive these from 'DNA codon table')
        STARTS = {'ATG'}
        STOPS = {'TAA', 'TGA', 'TAG'}
        CODON_LENGTH = 3

        # pairs delimiting coding regions, with positions of first coding codon and STOP codon
        # these positions are suitable for 0-based indexing
        orf_pairs = []

        NON_CODING = 'NON_CODING'
        CODING = 'CODING'
        # state of the search for ORFs
        state = NON_CODING
        # the start position of a coding region
        start_pos = None

        # codons start at positions that are multiples of CODON_LENGTH
        for codon_start in range(0, len(self.mini_chromosome), CODON_LENGTH):
            # ignore incomplete terminating codons
            if len(self.mini_chromosome) < codon_start + CODON_LENGTH:
                continue

            codon = self.mini_chromosome[codon_start: codon_start + CODON_LENGTH]

            if state == NON_CODING and codon in STARTS:
                start_pos = codon_start + CODON_LENGTH
                state = CODING

            elif state == CODING and codon in STOPS:
                stop_pos = codon_start
                orf_pairs.append((start_pos, stop_pos))
                state = NON_CODING

        return orf_pairs

test_cases = [(MiniChromosome('ATGTAA'), [(3, 3)]),
              (MiniChromosome('ATGAAATAA'), [(3, 6)]),
              (MiniChromosome('ATGATGTAA'), [(3, 6)]),
              (MiniChromosome('ATGATGTAAG'), [(3, 6)]),      # incomplete terminating codon
              (MiniChromosome('ATGAAAAAA'), []),             # unclosed ORF
              # multiple ORFs, trailing non-coding
              (MiniChromosome('CCC' + 'ATG' + 'C'*6 + 'TAG' + 'CCC' + 'ATG' + 'C'*9 + 'TGA' + 'CCC'),
               [(6, 12), (21, 30)])
             ]

def test_mc():
    for test_case in test_cases:
        mc, expected = test_case
        # print(mc.find_orfs(), expected)
        assert mc.find_orfs() == expected
test_mc()
