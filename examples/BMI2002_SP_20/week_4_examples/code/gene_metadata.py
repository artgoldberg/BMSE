# the line above tells Jupyter to write this cell to the file gene_metadata.py

import pandas
protein_dbms_file = 'HGNC_protein-coding_gene.tsv'
protein_dbms = pandas.read_table(protein_dbms_file, index_col=1, low_memory=False, )

def get_protein(protein_name):
    # get meta information about `protein_name`
    return protein_dbms.loc[protein_name]