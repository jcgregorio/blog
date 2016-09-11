#!/usr/bin/python2.4
import dispatch, os

print """Status: 200 Ok\nContent-type: text/plain\n\nJust testing.   more."""

print os.environ.get('PATH_INFO', '/')

print "\n".join(["%s=%s" % (key, value) for key, value in os.environ.iteritems()]) 

# dispatch based on the method

# process the path component, mapping it to a safe directory
# perform the requested operations 

# GET, dispatch based on the presence of a Range: header
# Also add in 'collection' members for each sub-directory.

# Dispatch HEAD along to the same op as GET.

# Use the dispatcher from Bulu.

# Remember to generate ETags 

# Remember to require ETags for PUTs


