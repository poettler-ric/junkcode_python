#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/peak.html

Challenge 5 shows a mountain, and advices you, to pronounce it. The source asks
you, whether "peak hell" sounds familiar, and a peakhell tag to a file.
"""

from contextlib import closing
from urllib import urlopen
import pickle

url = "http://www.pythonchallenge.com/pc/def/banner.p"

with closing(urlopen(url)) as page_file:
    data = pickle.loads(page_file.read())
    for row in data:
        line = ''
        for chunk in row:
            line += chunk[0] * chunk[1]
        print line
