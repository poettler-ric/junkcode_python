#!/usr/bin/python -tt

"""
http://www.pythonchallenge.com/pc/def/linkedlist.php

Challenge 4 shows a simple picture and in it's sourcecode:
<!-- urllib may help. DON'T TRY ALL NOTHINGS, since it will never 
end. 400 times is more than enough. -->
<a href="linkedlist.php?nothing=12345"><img src="chainsaw.jpg" border="0"/></a>
"""

from contextlib import closing
from urllib import urlopen
import re

url_pattern = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=%s"
next_number = 12345
old_number = -1

next_nothing_pattern = re.compile(r"and the next nothing is (\d+)")
def next_nothing(data, *args):
    return next_nothing_pattern.findall(data)[0]

tired_pattern = re.compile(\
    r"<font color=red>Your hands are getting tired </font>and the next nothing is (\d+)")
def tired(data, *args):
    return tired_pattern.findall(data)[0]

missleading_pattern = re.compile(\
    r"""There maybe misleading numbers in the 
text. One example is \d+. Look only for the next nothing and the next nothing is (\d+)""")
def missleading(data, *args):
    return missleading_pattern.findall(data)[0]

divide_pattern = re.compile(r"Yes. Divide by two and keep going.")
def divide(data, number, *args):
    return int(number) / 2

patterns = {next_nothing_pattern: next_nothing,
    tired_pattern: tired,
    missleading_pattern: missleading,
    divide_pattern: divide}

while next_number and next_number != old_number:
    old_number = next_number
    with closing(urlopen(url_pattern % next_number)) as url_file:
        page_content = url_file.read()
        print page_content
        for (pattern, function) in patterns.iteritems():
            matcher = pattern.match(page_content)
            if matcher:
                next_number = function(page_content, next_number)
                break
