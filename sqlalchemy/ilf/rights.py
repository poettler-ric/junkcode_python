#!/usr/bin/env python

from inet_old import get_session
from inet_old import Employee
import sys

if len(sys.argv) < 3:
    print "usage: %s <right> <type>" % sys.argv[0]
    exit()

right = sys.argv[1]
type = sys.argv[2]

print "listing employees for right: %s and type: %s" \
          % (right, type)

print sys.stdout.encoding
with get_session() as session:
    query = session.query(Employee)
    query = query.join('rights')
    query = query.filter_by(right_id=right)
    query = query.filter_by(type=type)
    for employee in query:
        print employee.__str__()
