#!/usr/bin/python

"""
Attempt to explain object oriented programming in python to new programmers
===========================================================================

Classes are templates/blueprints for things/data you want to represent. E.g.
if you need to handle multiple diffenrent persons you could define a class for
it. A person could have a name and a age.

A class is a blueprint. An instance created according to the blueprint of a
class is called object.
"""
class Person(object):
    def __init__(self, name, age):
        """This is called an 'initializer'. It might take some parameters (here
        a name an an age) and initializes the object.
        
        'self' always references the object itself.
        
        The name and age are saved in the object. name and age are called the
        object's/Person's properties.
        """
        self.name = name
        self.age = age

    def introduce(self):
        """Methods are basicly functions executed with the object as context.
        E.g. a person could introduce himself.

        'with the object as context' basically means it has access to the
        object's internal variables. E.g. the object of a person has access to
        it's name.

        Even if the method doesn't take any parameters 'self' must be defined to
        tell the interpreter on which object the method should be executed.

        Difference between method and function: A function mainly has just the
        parameters passed to it to work with. A method is 'attached' to an
        object and also has access to the objects properties.
        """
        print("My name is {}.".format(self.name))

    def say(self, something):
        """Defining a method taking another parameter."""
        print("{}: {}".format(self.name, something))

    def tell_age(self):
        """Methods can even call other methods of the same object."""
        self.say("My age is {}".format(self.age))

    def celebrate_birthday(self):
        """Objects can alter their data."""
        self.age += 1

    def __str__(self):
        """Human readable representation of the object. This is automatically
        used when e.g. printing the object."""
        return "Person(name: '{}', age {})".format(self.name, self.age)

class VIP(Person):
    def __init__(self, name, age, agent):
        super(VIP, self).__init__(name, age)
        self.agent = agent

    def tell_age(self):
        self.say("Won't tell!")

    def __str__(self):
        return "VIP(name: '{}', age: {}, agent: {})".format(self.name,
                                                            self.age,
                                                            self.agent)

if __name__ == '__main__':
    richi = Person("richi", 30)
    print(richi)
    print("Directly accessing name: {}".format(richi.name))
    richi.introduce()
    richi.name = "RICHI"
    richi.introduce()
    richi.name = "richi"
    richi.introduce()
    richi.say("Hello!")
    richi.tell_age()
    richi.say("Celebrating birthday")
    richi.celebrate_birthday()
    richi.tell_age()

    moritz = Person("Moritz", 10)
    moritz.say("Hello!")

    actor = VIP("Some Actor", 40, "His Agent")
    print(actor)
    actor.say("Something important")
    actor.tell_age()
    actor.say("Celebrating birthday")
    actor.celebrate_birthday()
    print(actor)
    actor.say("Getting a new agent")
    actor.agent = richi
    print(actor)
