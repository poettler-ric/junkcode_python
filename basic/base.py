#!/usr/bin/env python

"""
Converts a base10 number to another baseX String.
"""

import string
import sys

sign_map = string.digits + string.ascii_uppercase

if len(sys.argv) < 3:
    print "Usage:", sys.argv[0], "<base10 number> <baseX>"
    exit(1)

def to_base(num, base):
    remain = ''
    while num:
        remain = sign_map[num % base] + remain
        num = num / base
    return remain

print to_base(int(sys.argv[1]), int(sys.argv[2]))
