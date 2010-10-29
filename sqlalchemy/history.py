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
from sqlalchemy.orm.session import object_session


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

    def historize(self):
        history = NoteHistory()
        history.id = self.id
        history.text = self.text
        return history

class NoteHistory(object):
    def __repr__(self):
        return u"<NoteHistory: %s %s: %s %s>" \
                % (self.history_id, self.history_timestamp, self.id, self.text)

class HistoryExtension(MapperExtension):
    """
    Creates a history entry for the changed or deleted object.

    For an object to be historized it must implement a historize() method,
    which returns an instance of a history class with all fields of the actual
    object copied into it.
    The history class must then be mapped to a table containing at least the
    same fields as the original one. Additional fields can be specified, too.
    Like: ::

        Column('history_id', Integer, primary_key=True),
        Column('history_timestamp', DateTime, default=datetime.now),
    """
    def before_delete(self, mapper, connection, instance):
        session = object_session(instance)
        print "delete: ", instance
        session.add(instance.historize())
        return EXT_CONTINUE

    def before_update(self, mapper, connection, instance):
        session = object_session(instance)
        if not session.is_modified(instance, include_collections=False):
            return EXT_CONTINUE
        print "update: ", instance
        session.add(instance.historize())
        return EXT_CONTINUE

mapper(Note, notes_table, extension=HistoryExtension())
mapper(NoteHistory, notes_history_table)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()

if __name__ == '__main__':
    print "== test =="
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
