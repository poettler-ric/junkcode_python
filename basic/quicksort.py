#!/usr/bin/env python

"""
Quicksort in as view lines as possible.

http://gumuz.nl/weblog/obfuscated-python/
"""

import random

def q(l): return [] if not l else q([i for i in l[1:]if i<l[0]])+[l[0]]+q([i for i in l[1:]if i>=l[0]])

def sort(l):
    """Unobfuscated version."""
    if not l:
        return []
    else:
        return sort([i for i in l[1:] if i < l[0]]) \
            + [l[0]] \
            + sort([i for i in l[1:] if i >= l[0]])

numbers = range(10)
random.shuffle(numbers)
print numbers
print q(numbers)
