#!/usr/bin/python

import random

needle = random.randint(1, 10)
guess = -1

while guess != needle:
	guess = raw_input("guess a number: ")
	try:
		guess = int(guess.strip())
	except:
		print "not a number"
		continue
	if guess > needle:
		print "too big"
	elif guess < needle:
		print "too small"
print "guess (", guess, ") was correct"

