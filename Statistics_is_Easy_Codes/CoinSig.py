#!/usr/bin/python

######################################
# Coin Toss Significance Test
# From: Statistics is Easy! By Dennis Shasha and Manda Wilson
#
# Simulates 10,000 experiments, where each experiment is 17 tosses of a fair coin.
# For each experiment we count the number of heads that occur out of the 17 tosses.
# We then compare our observed number of heads in 17 tosses of a real coin to this
# distribution, to determine the probability that our sample came from this assumed
# distribution (to decide whether this coin is fair).
#
# Author: Manda Wilson
# Author: Arthur GOldberg
#
# Pseudocode:
#
# 1. Set a counter to 0, this will count the number of times we get 15 or more
#    heads out of 17 tosses.
#
# 2. Do the following 10,000 times:
#    a. Do the following for the number of trials, counting successes as we go:
#        i. Pick a random floating point number in the range [0.0, 1.0).
#        ii. If the number we drew is less or equal to the probability of heads then the draw is a success.
#    b. If the number of successes from step (2a) is greater than or equal to 15, increment our counter
#       from step (1).
#
# 3. counter / 10,000 equals the probability of getting an observed number of heads greater than or equal to 15
#    in 17 tosses if the coin is fair.
#
######################################

import random

######################################
#
# Adjustable variables
#
######################################

observed_number_of_heads = 15
number_of_tosses = 17
probability_of_head = 0.5

######################################
#
# Subroutines
#
######################################

# p = probability of some outcome for a trial
# n = number of trials
# returns number of times outcome with probability p occurred out of n trials
def applyprob(p, n):
	num_successes = 0
	for j in range(n):
		if random.random() <= p:
			num_successes += 1
	return num_successes

######################################
#
# Computations
#
######################################

countgood = 0
number_of_bootstraps = 10_000
num_of_heads = []

for i in range(number_of_bootstraps):
	num_of_heads.append(applyprob(probability_of_head, number_of_tosses))
	
# count the number of times we got greater than or equal to 15 heads out of 17 coin tosses
countgood = len([x for x in num_of_heads if x >= observed_number_of_heads])

######################################
#
# Output
#
######################################

print(countgood, "out of", number_of_bootstraps, "times we got at least", end=' ')
print(observed_number_of_heads, "heads in", number_of_tosses, "tosses.")
print("Probability that chance alone gave us at least", observed_number_of_heads, end=' ')
print("heads in", number_of_tosses, "tosses is", countgood / float(number_of_bootstraps), ".")
