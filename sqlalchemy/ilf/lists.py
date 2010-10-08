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

def list_companys():
    import pprint
    pp = pprint.PrettyPrinter()

    output_file = r'c:\temp\companies.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header = (
                    "id",
                    "name",
                    "layer",
                    "layer1",
                    "layer2",
                    "layer3",
                    "layer4",
                    "layer5",
                    "groupid",
                    "legal",
                    )
            csv_writer.writerow(header)

            locations = session.query(Location).all()
            for location in locations:
                group_query = session.query(Location)
                group_query = group_query.filter(Location.layer1==location.layer1)
                group_query = group_query.filter(Location.layer2==location.layer2)
                group_query = group_query.filter(Location.layer3==0)
                group_query = group_query.filter(Location.layer4==0)
                group_query = group_query.filter(Location.layer5==0)
                group_query = group_query.filter(Location.id_!=location.id_)
                group = group_query.first()
                rowdata = (
                        location.id_,
                        location.name,
                        location.get_layer(),
                        location.layer1,
                        location.layer2,
                        location.layer3,
                        location.layer4,
                        location.layer5,
                        group.id_ if group is not None else "",
                        'y' if location.is_legal else "n",
                        )
                csv_writer.writerow([unicode(cell if cell is not None else "")
                    for cell in rowdata])

if __name__ == '__main__':
    list_locations()
