#!/usr/bin/python

import os, sys

print "Content-type: text/plain"
print ""
print "\n".join(["%040s = %s" % (name, value) for (name, value) in os.environ.iteritems()])

print  str(sys.argv)
