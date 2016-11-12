#!/usr/bin/python3

"""Testing the config parser."""

from configparser import ConfigParser

CONFIG = """
[section1]
key1 = value1
"""

if __name__ == '__main__':
    config = ConfigParser() # pylint: disable=C0103
    config.read_string(CONFIG)
    print(config.get('section1', 'key1'))
