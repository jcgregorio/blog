#!/usr/bin/python -u

"""zipcode.cgi

A web service for validating zipcodes.

!!!!!!!!!!!!!!!!!!!!!
    DO NOT USE
!!!!!!!!!!!!!!!!!!!!!

This relies on a completely *outdated* list of zipcodes
from the census bureau. Do not use it. It is just
here as an example.

"""

__author__ = "Joe Gregorio (joe@bitworking.org)"
__copyright__ = "Copyright 2007, Joe Gregorio"
__contributors__ = []
__version__ = "1.0.0 $Rev:  $"
__license__ = "MIT"
__history__ = """

"""

from mmap import mmap
import os
from bisect import bisect_left
import sys


class Zipcodes(object):
    """Use mmap to treat the sorted file of zipcodes
    as an array"""
    def __init__(self):
        self.f = open("sortzips.txt", "r+")
        self.size = os.path.getsize("sortzips.txt")
        self.m = mmap(self.f.fileno(), self.size)

    def __getitem__(self, i):
        self.m.seek(6*i)
        return self.m.read(5)

    def __del__(self):
        self.m.close()
        self.f.close()

    def __len__(self):
        return self.size / 6

zipcodes = Zipcodes()
target = os.environ.get('PATH_INFO', '/')[1:]
found = ( zipcodes[bisect_left(zipcodes, target)] == target )

print "Status: " + ( found and "200 Ok" or "404 Not Found" )
print "Cache-control: max-age=172800"
print "Content-type: image/png"
print ""
f = open(found and "good.png" or "bad.png", "r")
png = f.read()
f.close()
sys.stdout.write(png)

