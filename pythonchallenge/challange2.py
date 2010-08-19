#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/ocr.html

Challange 2 shows a book and tells to look at the sourcecode of the page
"""

from contextlib import closing
from urllib import urlopen
import re

comment_pattern = re.compile(r"<!--(.*?)-->", re.DOTALL)
character_pattern = re.compile(r"[a-zA-Z]")

with closing(urlopen("http://www.pythonchallenge.com/pc/def/ocr.html")) as url_file:
	page_content = url_file.read()
	comments = comment_pattern.findall(page_content)
	solution = "".join(character_pattern.findall(comments[1]))
	print solution

