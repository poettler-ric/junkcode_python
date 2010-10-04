#!/usr/bin/env python

"""Simple test, how to write csv files"""

import csv
import sys

values = ({
    "key1": "val1",
    "key2": "val2",
    "key3": "val3",
    },
    {
    "key1": "val_1",
    "key2": "val_2",
    "key3": "val_3",
    },
    )

writer = csv.DictWriter(sys.stdout, values[0].keys())
writer.writerow(dict(zip(values[0].keys(), values[0].keys())))
for row in values:
    writer.writerow(row)
