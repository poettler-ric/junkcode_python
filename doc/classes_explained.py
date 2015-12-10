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

        Even if the method doesn't take any parameters 'self' must be defined
        to tell the interpreter on which object the method should be executed.

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

    def set_name(self, new_name):
        """Methods can also change the object's data with given values."""
        self.name = new_name

    def __str__(self):
        """Human readable representation of the object. This is automatically
        used when e.g. printing the object."""
        return "Person(name: '{}', age {})".format(self.name, self.age)


"""Classes can inherit properties and methods from another class. The new class
mostly is entiched with additional properties and methods or specialized for a
given usecase. This is called inheritance. The class which inherits is called
subclass, the class from which is inherited is called superclass.

E.g. We want to represent an actor. An actor is a more specialized version of a
person so we can take the blueprint of a person and enrich it with additional
functionality.

A subclass could be seen as a copy of the superclass overwritten/enriched with
new methods and properties."""


class VIP(Person):
    def __init__(self, name, age, agent):
        """Additional to a person's name a vip has an agent.

        First we initialize the superclass with the person's data. Then we save
        the agent property.
        """
        super(VIP, self).__init__(name, age)
        self.agent = agent

    def tell_age(self):
        """It is possible to overwrite methods of superclasses as needed. It in
        a subclass it is also possible to access methods of the superclass -
        here say(...).
        """
        self.say("Won't tell!")

    def __str__(self):
        """It is possible to access the superclasses' data - here name and
        age."""
        return "VIP(name: '{}', age: {}, agent: {})".format(self.name,
                                                            self.age,
                                                            self.agent)

if __name__ == '__main__':
    # create a new instance of the class Person
    richi = Person("richi", 30)
    # print the person. Internally this translates to richi.__str__().
    print(richi)
    # properties of an object can be accessed directly
    print("Directly accessing name: {}".format(richi.name))
    # executing a method on a given object
    richi.introduce()
    richi.say("Hello!")
    richi.tell_age()
    richi.say("Celebrating birthday")
    # calling a method which alters the objects properties (richi.age)
    richi.celebrate_birthday()
    richi.tell_age()

    # there are multiple ways to update properties of an object.
    richi.introduce()
    # either the author of the class wrote an explicit setter method
    richi.set_name("RICHI")
    richi.introduce()
    # or (the most common way in python) is to access the property
    # directly
    richi.name = "richi"
    richi.introduce()

    # defining a new person
    moritz = Person("Moritz", 10)
    # calling the same methods of two objects both access their own
    # properties (name)
    moritz.say("Hello!")
    richi.say("Hello!")

    # creating an instance of the class VIP (sublcass of Person)
    actor = VIP("Some Actor", 40, "His Agent")
    print(actor)
    # with a sublass you also have access to the superclass' methods
    actor.say("Something important")
    # calling a method overwritten by the subclass
    actor.tell_age()
    # but you can still access the age property...
    print("vip age: {}".format(actor.age))
    actor.say("Celebrating birthday")
    # ...and change it
    actor.celebrate_birthday()
    actor.age += 10
    print(actor)

    actor.say("Getting a new agent")
    # objects are just variables an can also be assigned to other
    # properties
    actor.agent = richi
    print(actor)
