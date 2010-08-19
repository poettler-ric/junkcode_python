#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/map.html

Challenge 1 shows a image of a piece of paper showing:
K -> M
O -> Q
E -> G

Below is the text saved in the string crypted.
"""

crypted = """g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc
dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle.
sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""

#crypted = "map"

decrypted = ""

characters_in_alphabet = 26

for letter in crypted:
	ascii_number = ord(letter)
	if ord('a') <= ascii_number and ascii_number <= ord('z'):
		ascii_number += 2
		if ord('z') < ascii_number:
			ascii_number -= characters_in_alphabet
		decrypted += chr(ascii_number)
	else:
		decrypted += letter
print decrypted
