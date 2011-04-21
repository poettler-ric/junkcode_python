#!/usr/bin/env python

from inet_old import Department
from inet_old import get_session
import csv


class UTF8Writer:
    def __init__(self, fileobj, **kwds):
        self.writer = csv.writer(fileobj, dialect=csv.excel, **kwds)

    def writerow(self, row):
        self.writer.writerow([cell.encode('utf-8') for cell in row])
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def location_department():
    output_file = r'c:\temp\location_department.csv'
    with open(output_file, "wb") as file_obj:
        csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
        with get_session() as session:
            query = session.query(Department)
            for department in query.all():
                if department.inactive != 0:
                    print "inactive: %s" % department.name
                    continue
                location = department.cost_center.location if department.cost_center else None
                csv_writer.writerow([location.name if location else "***", department.name])

if __name__ == '__main__':
    location_department()
