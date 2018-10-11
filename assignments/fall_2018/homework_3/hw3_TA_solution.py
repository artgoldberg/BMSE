#!/usr/bin/env python 

'''Solution to HW 3: Write a Python program, Biomedical Software Engineering, Mount Sinai School of Medicine

:Author: Ryan Neff ryan.neff@icahn.mssm.edu
:Author: Nicole Zatorski nicole.zatorski@icahn.mssm.edu
:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Date: 2018-10-10
'''

import sys
from numpy import mean

DNA_RNA = {"A":"A",
			"C":"C",
			"G":"G",
			"T":"U"}

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

START_CODON = set(["AUG"])

def trans_trans(chromosome, dna_rna=DNA_RNA, rna_protein=RNA_PROTEIN, start_codons=START_CODON):
	''' Translates a mini-chromosome (sequence of DNA nucleotides) to a protein,
		calculating some properties about it

		Inputs:
			chromosome (string) (required)
				An input sequence of A,C,T,G, all uppercase, as a string.
			dna_rna (dict) (optional)
				A dictionary to translate DNA to RNA, with DNA nucleotides as keys
				and RNA nucleotides as values.
			rna_protein (dict) (optional)
				A dictionary to translate RNA codons to AAs. The AAs output
				are single letters by default. STOP = end of translation.
			start_codons (set) (optional)
				A set of start codon strings that indicate the initiation of translation.

		Returns:
			data (dict) - A dict with the following keys:
				proteins (list)
					A list of the translated proteins
				number_proteins (dict)
					value (int)
						The number of proteins translated.
					units (str)
						A string identifying the units of the measurement.
				len_shortest_protein (dict)
					value (int)
						The length of the shortest protein.
					units (str)
						A string identifying the units of the measurement.
				len_longest_protein (dict)
					value (int)
						The length of the longest protein.
					units (str)
						A string identifying the units of the measurement.
				mean_protein_length (dict)
					value (float)
						The mean protein length of translated proteins.
					units (str)
						A string identifying the units of the measurement.
				DNA_failure (bool)
					Did a DNA failure occur in the strand?
				total_noncoding_bases (dict)
					value (int)
						The total number of non-coding bases.
					units (str)
						A string identifying the units of the measurement.
	'''

	#initialize variables
	proteins = []
	total_noncoding_bases = 0
	DNA_failure = False

	#check if input is valid
	if set([i for i in chromosome]).difference(set(list(dna_rna.keys()))) is None:
		raise KeyError("DNA nucleotides in input not translatable to RNA\
					 given the mapping dictionary.")

	#translate DNA to RNA
	rna_chromosome = "".join([dna_rna[i] for i in chromosome])

	translating = False
	for codon in [rna_chromosome[i:i+3] for i in range(0,len(rna_chromosome),3)]:
		if len(codon) != 3: 
			#if we have input with an odd # of bases, skip the last ones
			total_noncoding_bases += len(codon)
			break
		if not translating:
			if codon in start_codons: #if the codon is AUG
				translating=True #set to translating
				proteins.append([])
				continue
			else:
				total_noncoding_bases += 3
		else:
			if codon not in rna_protein:
				#check if the codon is translatable, otherwise raise an error
				raise KeyError("Codon %s not translatable to protein given the \
				               mapping dictionary."%codon)
			amino_acid = rna_protein[codon]
			if amino_acid == "STOP":
				translating = False
				continue
			proteins[-1].append(amino_acid)
	if (translating == True)|(len(proteins)==0):
		DNA_failure = True

	len_shortest = min([len(a) for a in proteins]) if len(proteins) > 0 else 0
	len_longest = max([len(a) for a in proteins]) if len(proteins) > 0 else 0
	mean_len = float(mean([len(a) for a in proteins])) if len(proteins) > 0 else 0.0

	protein_list = []
	for p in proteins:
		if p != []:
			protein_list.append("".join(p))
		else:
			DNA_failure = True

	data = {
		"proteins":protein_list,
		"number_proteins":{"value":len(protein_list),"units":"proteins"},
		"len_shortest_protein":{"value":len_shortest,"units":"amino acids"},
		"len_longest_protein":{"value":len_longest,"units":"amino acids"},
		"mean_protein_length":{"value":mean_len,"units":"amino acids"},
		"DNA_failure":DNA_failure,
		"total_noncoding_bases":{"value":total_noncoding_bases,"units":"bases"}
		}
	
	return data

def summary_stats(chromosomes, dna_rna=DNA_RNA, rna_protein=RNA_PROTEIN, start_codons=START_CODON):
	''' Take a list or tuple of chromosomes and returns the summary statistics for them
	
	Inputs:
		chromosomes (list or tuple)
			contains  an input (string) of A,C,T,G
		dna_rna (dict) (optional)
			A dictionary to translate DNA to RNA, with DNA nucleotides as keys
			and RNA nucleotides as values.
		rna_protein (dict) (optional)
			A dictionary to translate RNA codons to AAs. The AAs output
			are single letters by default. STOP = end of translation.
		start_codons (set) (optional)
			A set of start codon strings that indicate the initiation of translation.
	Outputs: 
		chromosomes_stats (dictionary)
			num_proteins (key, string)
				total number of encoded proteins (value, integer)
			len_shortest_protein (key, string)
				length of the shortest protein (value, integer) [units: amino acids]
			len_longest_protein (key, string)
				length of the longest protein (value, integer) [units: amino acids]
			mean_len (key, string)
				mean of the protein length (value, float if all DNA contains proteins and "unknown" otherwise) [units: amino acids]
			non_coding_DNA (key, string)
				total number of noncoding nucleotides (integer) [units: nucleotides]
			num_failures (key,string)
				number of transcription failures (integer)
			chromosome_data_dictionary (key, string)
				dictionary of the results of each chromosome input into trans_trans
				string of bases (A,C,T,G) corresponding to a chromosome (key, string)
					output of trans_trans function for the corresponding chromosome (value, dictionary) 
	'''
	chromosomes_data_dictionary = {}
	num_proteins = 0
	len_shortest_protein = None
	len_longest_protein = 0
	mean_len = 0
	non_coding_DNA = 0
	num_failures = 0


	for chromosome in chromosomes:
		chromosome_data = trans_trans(chromosome)

		num_proteins += chromosome_data['number_proteins']['value']

		if chromosome_data['len_shortest_protein']['value'] > 0:
			if len_shortest_protein == None:
				len_shortest_protein = chromosome_data['len_shortest_protein']['value']
			else:
				if len_shortest_protein > chromosome_data['len_shortest_protein']['value']:
					len_shortest_protein = chromosome_data['len_shortest_protein']['value']

		if len_longest_protein < chromosome_data['len_longest_protein']['value']:
			len_longest_protein = chromosome_data['len_longest_protein']['value']

		if mean_len != 'unknown':
			if chromosome_data['number_proteins']['value'] == 0:
				mean_len = 'unknown'
			else:
				mean_len += chromosome_data['number_proteins']['value']

		non_coding_DNA += chromosome_data['total_noncoding_bases']['value']

		if chromosome_data['DNA_failure']:
			num_failures += 1

		chromosomes_data_dictionary[chromosome] = chromosome_data

		

	if mean_len != 'unknown':
		mean_len = mean_len/num_proteins

	chromosomes_stats = {
		'chromosomes_data_dictionary':chromosomes_data_dictionary, 
		'number_proteins':{'value':num_proteins, 'units':'proteins'}, 
		'length_shortest_protein':{'value':len_shortest_protein, 'units':'amino acids'}, 
		'length_longest_protein':{'value':len_longest_protein, 'units':'amino acids'},
		'mean_protein_length':{'value':mean_len, 'units':'amino acids'}, 
		'total_noncoding_bases':{'value':non_coding_DNA, 'units':'bases'}, 
		'number_failures':num_failures}

	return chromosomes_stats

def print_result(result):
	individual_results = result.pop('chromosomes_data_dictionary')
	for key,val in individual_results.items():
		print('Chromosome')
		print('  ', key)
		for k,v in val.items():
			print(k)
			print('  ', v)
		print("========================")
	print('Sumary Statistics')
	print('***********************')
	for key,val in result.items():
		print(key)
		print("  ",val)
	print("========================")
	return ""

if __name__=="__main__":

	'''print_result(summary_stats([
		"ATGGAACAAGAATGA", 
		"ATGATTTAAATGATCTAAATGATTTAA",
		"CATATGATTATTTAAATCATGATTATTTAGGATATGGATATTTAGATT",
		"ATGATTATGTAA",
		"ATTATGTAA"]))
'''
    # some test cases:
	# print("Sequence 1: DNA with 1 protein that's 3 AA long; no non-coding DNA")
	# print_result(summary_stats(["ATGGAACAAGAATGA"]))

	# print("Sequence 2: DNA with 3 proteins, each 1 AA long; no non-coding DNA")
	# print_result(summary_stats(["ATGATTTAAATGATCTAAATGATTTAA"]))

	# print("Sequence 3: DNA with 3 proteins, each 2 AA long; initial and trailing non-coding DNA, and between the proteins")
	# print_result(summary_stats(["CATATGATTATTTAAATCATGATTATTTAGGATATGGATATTTAGATT"]))

	# print("Sequence 4: DNA with 1 protein, 2 AA long, containing a methionine encoded by ATG; no non-coding DNA")
	# print_result(summary_stats(["ATGATTATGTAA"]))

	# print("Sequence 5: DNA with no protein")
	# print_result(summary_stats(["ATTATGTAA"]))

	# print("DNA with a 0-length protein; no non-coding DNA")
	# print_result(summary_stats(["ATGTAA"]))

	# print("DNA with 1 protein that's 1 AA long; trailing non-coding DNA")
	# print_result(summary_stats(["ATGCGTTAACGT"]))

	# print("DNA with 1 protein that's 1 AA long; trailing non-coding DNA; nucleotides not a multiple of 3")                          
	# print_result(summary_stats(["ATGCGTTAACGTA"]))

	# print("DNA failure: no start codon")                                
	# print_result(summary_stats(["ATTAGGTAA"]))

	# print("DNA failure: ends while encoding a protein")                                
	# print_result(summary_stats(["ATGCGTCGT"])) 


