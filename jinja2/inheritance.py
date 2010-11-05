#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
from datetime import date

class Note(object):
    def __init__(self, author, date, message):
        self.author = author
        self.message = message
        self.date = date

    def __repr__(self):
        return u"Note(author: %s date: %s message: %s)" \
                % (self.author, self.date, self.message)

notes = (
        Note("richi", date.today(), "first note"),
        Note("mike", date.today(), "where is data?"),
        Note("georg", date.today(), "let's talk about it"),
        )
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('list_notes.html')
print template.render(notes=notes)
