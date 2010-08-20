#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/equality.html

Challenge 3 shows a picture of 7 candles, where the middle one is the only
small one. Beneath that is a text: "One small letter, surroundet by *EXACTLY*
three big bodyguards on each of it's sides"
"""

from contextlib import closing
from HTMLParser import HTMLParser
from urllib import urlretrieve
import gzip
import os
import re

url = "http://www.pythonchallenge.com/pc/def/equality.html"
filename = "temp.gz"

bodyguard_pattern = re.compile(r"[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]")

class HTMLCommentLettersParser(HTMLParser):
    def handle_comment(self, data):
        print "".join(bodyguard_pattern.findall(data))

urlretrieve(url, filename)
with closing(gzip.open(filename)) as zipfile:
    with closing(HTMLCommentLettersParser()) as parser:
        parser.feed(zipfile.read())
os.remove(filename)
