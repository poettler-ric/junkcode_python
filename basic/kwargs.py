#!/usr/bin/env python

class Test(object):
    def __init__(self, **kwargs):
        print "got: ", kwargs
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return u"<Test: %s %s %s>" % (self.val1, self.val2, self.val3)

print Test(val1="first-value", val2="second-value", val3="third-value")
