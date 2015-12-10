#!/usr/bin/python


class Namespace(dict):
    """A simple namespace implementation."""
    def __init__(self, values={}):
        super(Namespace, self).__init__(values)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError("attribute {} not defined".format(name))

    def __setattr__(self, name, value):
        self[name] = value

    def say(self):
        """Method to test whether we can overwrite existing methods with new
        attributes.
        """
        print("hello")

if __name__ == '__main__':
    ns = Namespace({'b': 10})
    ns.a = 5
    print ns.a
    print ns.b

    print "= testing overwrite"
    print ns.say
    ns.say()
    print "= overwriting"
    ns.say = "asdf"
    print ns.say
    ns.say()
