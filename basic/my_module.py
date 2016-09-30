"""
Dummy module to show, when which code gets executed.
"""

def my_function():
    """Example module function"""
    print("= inside function")

class MyClass:
    """Example Class"""
    print("= inside class")

    def __init__(self):
        """Empty initializer"""
        print("= inside constructor")

    def my_method(self):
        """Example method"""
        print("= inside method")

    @staticmethod
    def my_class_function():
        """Example static function"""
        print("= inside class function")

print("= inside module (e.g. some calculations)")
if __name__ == '__main__':
    print("= inside main guard")
