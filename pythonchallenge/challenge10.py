#!/usr/bin/env python

"""
http://www.pythonchallenge.com/pc/return/bull.html

Challenge 10 shows a picture of a cow with the question about the length of the
element at index 30 of a list like:

a = (1, 11, 21, 1211, 111221, ...
"""

from itertools import groupby

value = "1"

for i in xrange(30):
    value = "".join(str(sum(1 for _ in v)) + k for k, v in groupby(value))

print len(value)
