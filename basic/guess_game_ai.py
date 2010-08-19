#!/usr/bin/python

import random

def average(*args):
	"""returns the average value of all supplied values."""
	return sum(args) / len(args)

minNumber = 1
maxNumber = 100

needle = random.randint(minNumber, maxNumber)
guess = -1

while guess != needle:
	guess = average(minNumber, maxNumber)

	if guess > needle:
		print guess, "is too big"
		maxNumber = guess
	elif guess < needle:
		print guess, "is too small"
		minNumber = guess
print "guess (", guess, ") was correct"
