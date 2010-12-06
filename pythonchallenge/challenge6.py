#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/channel.html

"""

from contextlib import closing
from urllib import urlopen
import pickle
from pprint import pprint

url = "http://www.pythonchallenge.com/pc/def/channel.html"
dump_file_name = r"c:\Temp\dump.zip"

with closing(urlopen(url)) as page_file:
    data = page_file.read()
    with open(dump_file_name, 'wb') as dump_file:
        dump_file.write(data)
    #unpickled = pickle.loads(data)
    #pprint(unpickled)
