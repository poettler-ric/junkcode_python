#!/usr/bin/env python

"""
Trying out some weird behaviour with python and class members which are
sometimes static, or not.
"""

class Plain:
    value = 0
    
    def incr(self):
        self.value += 1

    def __repr__(self):
        return "<Plain: %s>" % self.value

print Plain.value

print "--- set value through the class to 5"
Plain.value = 5

print "--- create new objects"
obj0 = Plain()
obj1 = Plain()
print obj0, obj1, obj0.value, obj1.value, Plain.value

print "--- increment obj0"
obj0.incr()
print obj0, obj1, obj0.value, obj1.value, Plain.value

print "--- set value through the class to 10"
Plain.value = 10

print "--- increment obj1"
obj1.incr()
print obj0, obj1, obj0.value, obj1.value, Plain.value

print "--- set value through the class to -5"
Plain.value = -5
print "--- set obj0's value through the object to -1"
obj0.value = -1
print obj0, obj1, obj0.value, obj1.value, Plain.value

print "--- creating a completely new object"
obj2 = Plain()
print obj2
