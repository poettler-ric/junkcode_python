#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/map.html

Challenge 1 shows a image of a piece of paper showing:
K -> M
O -> Q
E -> G

Below is the text saved in the string crypted.
"""

import string

crypted = """g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc
dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle.
sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""

table = string.maketrans(string.ascii_lowercase,
	string.ascii_lowercase[2:] + string.ascii_lowercase[:2])
print string.translate(crypted, table)

