#!/usr/bin/env python

"""Experiment with the dir function."""
def fields(obj):
    """Return all public fields of an object."""
    return filter(lambda x: not x.startswith('_'), dir(obj))

class Test(object):
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2

test = Test("a", "b")
print dir(test)
print "filtered:"
for field in fields(test):
    print field, '=', getattr(test, field)
