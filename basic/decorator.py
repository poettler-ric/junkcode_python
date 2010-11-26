#!/usr/bin/env python

def decorator(*decorator_arguments):
    def decorate(old_function):
        def new_function(*args, **kwargs):
            print "=== executing decorator"
            print "decorator_arguments:", decorator_arguments
            print "function arguments:", args, kwargs
            print "=== getting result"
            result = old_function(*args, **kwargs)
            return result
        return new_function
    return decorate

@decorator("aa", "bb")
def add(a, b):
    return a + b

print add(2, 4)
