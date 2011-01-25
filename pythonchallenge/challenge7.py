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
max_area_width = 7 # we assume the maximum area width (for double letters)
R, G, B, A = 0, 1, 2, 3 # red, green, blue, alpha
X, Y = 0, 1

urllib.urlretrieve(url, file_name)

image = Image.open(file_name)
pixels = image.load()

# determine the fist grey pixel in the first row
begin_y = -1
for i in xrange(image.size[Y]):
    pixel = pixels[0, i]
    if pixel[R] == pixel[G] == pixel[B]:
        begin_y = i
        break

# determine the last nongrey pixel in the grey row
end_x = -1
for i in xrange(image.size[X]):
    pixel = pixels[i, begin_y]
    if not pixel[R] == pixel[G] == pixel[B]:
        end_x = i
        break

collected = ""
# iterate over the grey bar
for i in xrange(0, end_x, max_area_width):
    collected += chr(pixels[i, begin_y][R])

print collected

# extract the list in the string
ascii_list = eval(collected[collected.find('[') : collected.find(']') + 1])
print "the solution is:", ''.join(map(chr, ascii_list))

os.remove(file_name)
