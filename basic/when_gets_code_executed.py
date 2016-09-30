"""
Dummy program which imports a module and shows when which code gets executed.
"""

print("importing")
import my_module

print("instanciating")
my_instance = my_module.MyClass()

print("calling method")
my_instance.my_method()

print("calling class function")
my_module.MyClass.my_class_function()
