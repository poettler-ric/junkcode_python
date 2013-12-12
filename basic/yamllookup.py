#!/usr/bin/python

import sys
import yaml

if len(sys.argv) < 3:
    sys.exit("Usage: {} <filename> <keys>".format(sys.argv[0]))

separator = '.'
fileName = sys.argv[1]
keys = sys.argv[2]

path = keys.split(separator)

with open(fileName, 'r') as f:
    value = yaml.load(f)
    for key in path:
        value = value.get(key)
        if not value:
            sys.exit("Couldn't find key '{}' from '{}' in '{}'"
                .format(key, keys, fileName))
    print(value)
