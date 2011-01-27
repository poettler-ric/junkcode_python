#!/usr/bin/python

"""
http://www.pythonchallenge.com/pc/def/integrity.html

Challenge 8 shows a picture of a bee and ask you, where the link is.
"""

from contextlib import closing
from HTMLParser import HTMLParser
import bz2
import os.path
import re
import urllib2

class Challange8HTMLParser(HTMLParser):
    """
    Extracts username, password and the link for the next page out of the
    current html sourcecode. The values will be saved in the username, password
    and href attributes of the parser.
    """

    logindata_pattern = re.compile(r"un: ('[^']+')\npw: ('[^']+')")

    def handle_comment(self, data):
        """
        Extract the bzip compressed username and password out of the page
        comment.
        """
        match = self.logindata_pattern.search(data)
        if match:
            # eval because the strings now have the hex values escaped
            self.username = bz2.decompress(eval(match.group(1)))
            self.password = bz2.decompress(eval(match.group(2)))

    def handle_starttag(self, tag, attrs):
        """
        Extracts the href attribute out of the area tag.
        """
        if tag == "area":
            for key, value in attrs:
                if key == "href":
                    self.href = value
                    break

url = "http://www.pythonchallenge.com/pc/def/integrity.html"

with closing(urllib2.urlopen(url)) as page:
    with closing(Challange8HTMLParser()) as parser:
        # parse the actual page for the data
        parser.feed(page.read())

        to_open = os.path.join(os.path.dirname(url), parser.href)

        # construct the urlopener with the password handler
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, to_open, parser.username,
                parser.password)
        basic_handler = urllib2.HTTPBasicAuthHandler(password_manager)
        opener = urllib2.build_opener(basic_handler)

        # finally read the content of the new challenge
        with closing(opener.open(to_open)) as content:
            print content.read()

        print "username:", parser.username
        print "password:", parser.password
        print "new link:", to_open
