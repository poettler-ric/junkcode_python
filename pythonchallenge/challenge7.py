#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/oxygen.html

Challenge 7 shows a image of a river with a grey bar. The title says "smarty".
"""

from PIL import Image
import os
import tempfile
import urllib

url = "http://www.pythonchallenge.com/pc/def/oxygen.png"
file_name = tempfile.mktemp('-challenge7')

urllib.urlretrieve(url, file_name)

box_coordinates = (0, 43, 608, 52) # left, upper, right, lower pixels
image = Image.open(file_name)
box_pixels = image.crop(box_coordinates).load()

last_value = ord(' ') # initialize with a space
max_area_with = 7 # we assume the maximum area with (for double letters)
count = 0
collected = ""

for i in xrange(box_coordinates[2]):
    value = box_pixels[i, 0][0]
    if value != last_value or count >= max_area_with:
        collected += chr(last_value)
        last_value = value
        count = 1
    else:
        count += 1

print collected

ascii_list = eval(collected[collected.find('[') : collected.find(']') + 1])
print "the solution is:", ''.join(map(chr, ascii_list))

os.remove(file_name)
