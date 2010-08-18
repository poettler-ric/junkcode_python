#!/usr/bin/python

"""
Shows the sample usage of SQLAlchemy. Additionally shows the usage of a
SQLAlchemy-Context.

The thing to keep in mind is, that it happens, that there is a explicit commit
before closing the session
"""

from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from sqlalchemy.orm import mapper, sessionmaker

class Note(object):
	""" Dummy class holding some values """
	def __init__(self, author, text):
		self.text = text
		self.author = author

	def __repr__(self):
		return "<'%s' by %s>" % (self.text, self.author)

engine = create_engine('sqlite://', echo=True)
metadata = MetaData(engine)

notes_table = Table('notes', metadata,
	Column('id', Integer, primary_key=True),
	Column('author', String),
	Column('text', String))

metadata.create_all()
mapper(Note, notes_table)

Session = sessionmaker(bind=engine)

@contextmanager
def sqlSession():
	""" Contextmanager only closing the session. """
	session = Session()
	try:
		yield session
	finally:
		session.close()

@contextmanager
def sqlSessionFlush():
	""" Contextmanager only flushing the session. """
	session = Session()
	try:
		yield session
		session.flush()
	finally:
		session.close()

@contextmanager
def sqlSessionCommit():
	""" Contextmanager only committing the session. """
	session = Session()
	try:
		yield session
		session.commit()
	finally:
		session.close()

print "== no flush and no commit"
with sqlSession() as session:
	query = session.query(Note)
	for note in query:
		print "--", note
	session.add(Note("1st", "nothing"))
	session.add(Note("2nd", "nothing"))

print "== only flush"
with sqlSessionFlush() as session:
	query = session.query(Note)
	for note in query:
		print "--", note
	session.add(Note("3rd", "flush"))
	session.add(Note("4th", "flush"))

print "== only commit"
with sqlSessionCommit() as session:
	query = session.query(Note)
	for note in query:
		print "--", note
	session.add(Note("5th", "commit"))
	session.add(Note("6th", "commit"))


print "== querying again"
with sqlSessionCommit() as session:
	query = session.query(Note)
	for note in query:
		print "--", note
