#!/usr/bin/python3

"""Recursively walk through dicts read from a yaml file."""

from sys import argv
from yaml import load

if len(argv) < 3:
    exit("Usage: {} <file_name> <keys>".format(argv[0]))

SEPARATOR = '.'
file_name = argv[1] # pylint: disable=C0103
keys = argv[2] # pylint: disable=C0103

path = keys.split(SEPARATOR) # pylint: disable=C0103

with open(file_name, 'r') as f:
    value = load(f) # pylint: disable=C0103
    for key in path:
        value = value.get(key)
        if not value:
            exit("Couldn't find key '{}' from '{}' in '{}'"
                 .format(key, keys, file_name))
    print(value)
