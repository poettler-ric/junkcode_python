#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/channel.html
"""

import os
import os.path
import shutil
import tempfile
import urllib
import zipfile
import re

url = "http://www.pythonchallenge.com/pc/def/channel.zip"
file_name = os.path.basename(url)
#file_name = tempfile.mktemp('-challenge6')

directory_name = tempfile.mkdtemp('-challenge6')
#os.mkdir(directory_name)

next_file = '90052.txt' # taken from readme.txt in the zip

next_pattern = re.compile(r'Next nothing is (\d+)')

#urllib.urlretrieve(url, file_name)

files = None

with open(file_name) as file:
    zip = zipfile.ZipFile(file)
    files = set(zip.namelist())
    zip.extractall(directory_name)

while next_file:
    files.remove(next_file)
    with open(os.path.join(directory_name, next_file)) as file:
        content = file.read()
        print content

        match = next_pattern.match(content)
        if match:
            next_file = match.group(1) + '.txt'
        else:
            next_file = None

print files

#os.remove(file_name)
shutil.rmtree(directory_name)
