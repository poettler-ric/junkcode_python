#!/usr/bin/env python

""" Testing relations in SA.  """

from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper, sessionmaker, relationship

engine = create_engine(r'sqlite://', echo=True)
metadata = MetaData(engine)

author_table = Table('author', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        )
note_table = Table('note', metadata,
        Column('id', Integer, primary_key=True),
        Column('author_id', Integer, ForeignKey('author.id')),
        Column('note', String),
        )

class Author(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<author: %s>" % (self.name)

class Note(object):
    def __init__(self, note):
        self.note = note

    def __repr__(self):
        return "<note: %s>" % (self.note)

mapper(Author, author_table, properties={
    #'notes': relationship(Note, backref='author') # both work
    })
mapper(Note, note_table, properties={
    'author': relationship(Author, backref='notes') # both work
    })


metadata.drop_all()
metadata.create_all()
Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()

with get_session() as session:
    richi = Author("richi")
    michael = Author("michael")
    session.add(richi)
    session.add(michael)

    n1 = Note("test0")
    n2 = Note("test1")
    n3 = Note("test2")
    n4 = Note("test3")
    session.add(n1)
    session.add(n2)
    session.add(n3)
    session.add(n4)

with get_session() as session:
    session.query(Note).get(1).author = richi
    session.query(Note).get(2).author = michael
    session.query(Note).get(3).author = richi
    session.query(Note).get(4).author = michael

with get_session() as session:
    for author in session.query(Author):
        print "==", author
        print "==", author.notes
