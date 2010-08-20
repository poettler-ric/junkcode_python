#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/ocr.html

Challenge 2 shows a book and tells to look at the sourcecode of the page
"""

from contextlib import closing
from HTMLParser import HTMLParser
from urllib import urlopen
import string

url = "http://www.pythonchallenge.com/pc/def/ocr.html"

class HTMLCommentLettersParser(HTMLParser):
	def handle_comment(self, data):
		print "====="
		print filter(lambda x: x in string.letters, data)

with closing(urlopen(url)) as url_file:
	with closing(HTMLCommentLettersParser()) as parser:
		parser.feed(url_file.read())

