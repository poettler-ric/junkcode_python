#!/usr/bin/env python

from inet_old import get_session
from inet_old import Location

import csv


class UTF8Writer:
    def __init__(self, fileobj, **kwds):
        self.writer = csv.writer(fileobj, dialect=csv.excel, **kwds)

    def writerow(self, row):
        self.writer.writerow([cell.encode('utf-8') for cell in row])
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def list_locations():
    output_file = r'c:\temp\locations.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header=(
                    "id",
                    "name",
                    "street",
                    "zip",
                    "city",
                    "country",
                    )
            csv_writer.writerow(header)

            locations = session.query(Location).all()
            for location in locations:
                address = location.address
                country = address.country if address else None
                rowdata = (
                        location.id_,
                        location.name,
                        address.street if address is not None else None,
                        address.zip_code if address is not None else None,
                        address.city if address is not None else None,
                        country.name if country is not None else None,
                        )
                csv_writer.writerow([unicode(cell if cell is not None else "")
                    for cell in rowdata])

if __name__ == '__main__':
    list_locations()
