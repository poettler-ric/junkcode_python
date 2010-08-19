"""
Dummy module to show, when which code gets executed.
"""

def my_function():
	print "= inside function"

print "= inside module"

class MyClass:
	print "= inside class"

	def __init__(self):
		print "= inside constructor"

	def my_method(self):
		print "= inside method"
	
	@staticmethod
	def my_class_function():
		print "= inside class function"
