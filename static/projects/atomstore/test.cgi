#!/usr/bin/python

import os, sys

print "Content-type: text/plain"
print 'ETag: "notreallyanetag"'
print 'Status: 200 Ok'
print 'WWW-Authenticate: Basic realm="WallyWorld"'
print ""
print "\n".join(["%040s = %s" % (name, value) for (name, value) in os.environ.iteritems()])

print  str(sys.argv)
