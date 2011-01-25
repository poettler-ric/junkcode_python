#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/channel.html

Challenge 6 shows a image of a zip and some hints in the html source.
"""

import os
import tempfile
import urllib
import zipfile
import re

url = "http://www.pythonchallenge.com/pc/def/channel.zip"
file_name = tempfile.mktemp('-challenge6')
next_file = '90052.txt' # taken from readme.txt in the zip
next_pattern = re.compile(r'^Next nothing is (\d+)$')

urllib.urlretrieve(url, file_name)

comment = None
collected = ""

with zipfile.ZipFile(file_name, 'r') as zip:
    while next_file:
        content = zip.read(next_file)
        match = next_pattern.match(content)
        collected += zip.getinfo(next_file).comment
        if match:
            next_file = match.group(1) + '.txt'
        else:
            print content
            next_file = None

print collected

os.remove(file_name)
