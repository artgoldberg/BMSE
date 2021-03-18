"""Read FASTA files

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2021-03-13
"""

import os


class FastaReader:
  """Robustly read FASTA files that satisfy the standard in BLAST, Accepted Input Formats.

     See the standard at: https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=BlastHelp
     Raise exceptions for illegal FASTA files.
  """

  # define valid extensions
  # See https://en.wikipedia.org/wiki/FASTA_format
  VALID_EXTENSIONS = set(('fasta', 'fna', 'ffn', 'txt', 'frn'))
  VALID_NUCLEOTIDES = set(('A', 'C', 'G', 'T'))

  def __init__(self, pathname):
    """Initialize a FASTA file reader, and validate the pathname.

    Args:
        pathname: Pathname to the FASTA file.

    """
    self.pathname = pathname
    self.validate()

  def validate(self):
    """Validate the pathname to the FASTA file.

    Returns:
        A FastaReader with a validated pathname, to support chaining.

    Raises:
        ValueError: The pathname to the FASTA file is illegal.
    """
    # error if pathname isn't a string
    if not isinstance(self.pathname, str):
      raise ValueError(f"FASTA pathname isn't a string: '{self.pathname}'")

    # error if pathname isn't a file
    if not os.path.isfile(self.pathname):
      raise ValueError(f"FASTA pathname isn't a file: '{self.pathname}'")

    self.pathname = os.path.realpath(self.pathname)

    return self

  def read(self):
    """Read the FASTA file.

    Returns:
        A list of sequences in the FASTA file.

    Raises:
        ValueError: The FASTA file's contents are illegal.
    """
    try:
      fasta_file = open(self.pathname, 'r')
    except PermissionError as e:
      raise PermissionError(f"Cannot read FASTA file: '{self.pathname}'")

    lines = fasta_file.readlines()
    num_lines = len(lines)
    sequences = []

    for line_num in range(num_lines):

      # error if next line does not start with '>'
      if not lines[line_num].startswith('>'):
        raise ValueError(f"{line_num + 1}: missing description line that starts with '>'")

      if line_num >= num_lines:
        raise ValueError(f"{line_num + 2}: empty sequence")

      ## invariant: ready to read a non-empty sequence
      line_num += 1

      # read next sequence
      sequence = []
      # while (next line exists and does not start with '>')
      while line_num < num_lines and not lines[line_num].startswith('>'):
        line = lines[line_num].strip()

        # error if line is not nucleotides
        if set(line) - self.VALID_NUCLEOTIDES:
          raise ValueError(f"{line_num + 1}: invalid nucleotides "
                           f"{sorted(set(line) - self.VALID_NUCLEOTIDES)}")

        sequence.append(line)
        line_num += 1
      ## invariant: obtained non-empty sequence of nucleotides
      # add sequence to list of sequences
      sequences.append(''.join(sequence))

    return sequences
