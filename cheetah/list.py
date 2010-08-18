#!/usr/bin/python

from Cheetah.Template import Template

class Person:
	def __init__(self, firstName, surName):
		self.firstName = firstName
		self.surName = surName

	def __repr__(self):
		return "<%s %s>" % (self.firstName, self.surName)

persons = (Person("first_" + i, "sur_" + i) for i in ("a", "b", "c"))

print Template(file='templates/listPersons.tmpl',
		searchList={'persons': persons})
