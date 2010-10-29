#!/usr/bin/env python

"""
Shows a possibility to version database entries.
"""

from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm import EXT_CONTINUE
from sqlalchemy.orm.interfaces import MapperExtension

engine = create_engine("sqlite://")
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)

notes_table = Table('notes', metadata,
        Column('id', Integer, primary_key=True),
        Column('text', String),
        )

notes_history_table = Table('notes_history', metadata,
        Column('history_id', Integer, primary_key=True),
        Column('history_timestamp', DateTime, default=datetime.now),
        Column('id', Integer),
        Column('text', String),
        )

metadata.create_all()

class Note(object):
    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        return u"<Note: %s %s>" % (self.id, self.text)

class NoteHistory(Note):
    def __init__(self, note):
        Note.__init__(self, note.text)
        self.id = note.id
        
    def __repr__(self):
        return u"<NoteHistory: %s %s: %s %s>" \
                % (self.history_id, self.history_timestamp, self.id, self.text)

from sqlalchemy.orm.session import object_session

class HistoryExtension(MapperExtension):
    def __init__(self, history_class):
        self.history_class = history_class

    def before_delete(self, mapper, connection, instance):
        print "delete: ", instance
        session.add(self.history_class(instance))
        return EXT_CONTINUE

    def before_update(self, mapper, connection, instance):
        session = object_session(instance)
        if not session.is_modified(instance, include_collections=False):
            return EXT_CONTINUE
        print "update: ", instance
        session.add(self.history_class(instance))
        return EXT_CONTINUE

mapper(Note, notes_table, extension=HistoryExtension(NoteHistory))
mapper(NoteHistory, notes_history_table)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()

with get_session() as session:
    print "== adding"
    session.add(Note("asdf"))
    session.add(Note("foo"))
    session.add(Note("bar"))
    session.add(Note("test"))

with get_session() as session:
    print "== listing"
    for note in session.query(Note).all():
        print note

with get_session() as session:
    print "== modifying"
    note = session.query(Note).get(2)
    print note
    note.text = "new text"
    print note

with get_session() as session:
    print "== modifying with same values"
    note = session.query(Note).get(2)
    print note
    note.text = "new text"
    print note

with get_session() as session:
    print "== deleting"
    session.delete(session.query(Note).get(3))

with get_session() as session:
    print "== history"
    for note_history in session.query(NoteHistory).all():
        print note_history
