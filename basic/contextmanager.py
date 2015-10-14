#!/usr/bin/python

class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Person with name: %s" % self.name

    def __enter__(self):
        print("%s was born" % self.name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("%s died" % self.name)

with Person("richi") as p:
    print("%s is alive" % p)
