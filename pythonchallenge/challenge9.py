#!/usr/bin/env python

"""
http://www.pythonchallenge.com/pc/return/good.html

Challenge 8 shows a picture of a tree, with some weird dots.
"""

from challenge8 import getChallenge9Source
from contextlib import closing
from itertools import repeat
import cairo
import HTMLParser
import re

class Challenge9HTMLParser(HTMLParser.HTMLParser):
    """
    Extracts the first and second list out of the page's html comments. The
    lists will be stored in the first and second attributes of the parser.
    """

    """Pattern to extract the lists out of the comments."""
    value_pattern = re.compile(r"first:\n([\d,\n]+).*second:\n([\d,\n]+)")

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)

        self.comment_counter = 0

    def handle_comment(self, data):
        """
        Extract the first and second lists out of the page's comments.
        """
        self.comment_counter += 1

        if self.comment_counter == 2:
            matcher = self.value_pattern.search(data)
            if matcher:
                self.first = eval(matcher.group(1).replace('\n', ''))
                self.second = eval(matcher.group(2).replace('\n', ''))


def sublist(iterable, size=2):
    """
    Divides a list into sublists of a given size. Resulting sublists not
    matching the given size will be filled with None.

    sublist([0, 1, 2, 3, 4], 3) => (0, 1, 2), (3, 4, None)
    """
    pool = tuple(iterable)
    length = len(pool)
    start = 0
    while start < length:
        end = start + size
        if end <= length:
            yield pool[start:end]
        else:
            yield pool[start:] + tuple(repeat(None, end - length))
        start = end


max_x = max_y = 500 # we estimate a maximum drawing area of 500x500 pixels
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, max_x, max_y)
context = cairo.Context(surface)

# paint background
context.rectangle(0, 0, max_x, max_y)
context.set_source_rgb(1, 1, 1)
context.fill()

with closing(Challenge9HTMLParser()) as parser:
    parser.feed(getChallenge9Source())

    # paint black lines
    iterator = sublist(parser.first)
    x, y = iterator.next()
    context.move_to(x, y)
    for x, y in iterator:
        context.line_to(x, y)

    context.set_source_rgb(0, 0, 0)
    context.stroke()

    # paint blue lines
    iterator = sublist(parser.second)
    x, y = iterator.next()
    context.move_to(x, y)
    for x, y in iterator:
        context.line_to(x, y)

    context.set_source_rgb(0, 0, 1)
    context.stroke()

surface.write_to_png("bull.png")
