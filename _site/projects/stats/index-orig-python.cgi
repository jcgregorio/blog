#!/usr/bin/python2.4
import sys
sys.path.extend(['/home/jcgregorio/lib/python2.4/site-packages/','/home/jcgregorio/lib/python2.4/'])

import time
import re
import kid
from xml.sax.saxutils import escape
import cgi

form = cgi.FieldStorage()
offset = 0
if form.has_key("d"):
    offset = -int(form["d"].value)

reg = re.compile('\S* \S* \S* \[.*?\] \"GET /news/([a-zA-Z0-9_\/-]+) .*?\" \S*? \S*? \"(.*?)\"')
prjreg = re.compile('\S* \S* \S* \[.*?\] \"GET /projects/([a-zA-Z0-9_\-]+)/ .*?\" \S*? \S*? \"(.*?)\"')

now = time.time()
now += 24*60*60*offset
today = time.localtime(now)
filename = time.strftime("/home/jcgregorio/log/bitworking.org/%Y%m%d.log", today)

totals = {}
for line in file(filename, "r"):
    m = reg.search(line)
    if not m:
        m = prjreg.search(line)
    if m:
        (name, referrer) = m.groups()
        ref = totals.get(name, {})
        ref[referrer] = ref.get(referrer, 0) + 1
        if name not in totals:
            totals[name] = ref

print "Status: 200 ok"
print "Content-type: text/html"
print ""

print """<html>
   <head>
   </head>
   <body>
      <dl>
"""
kvp = [(sum([count for (uri, count) in ref.iteritems()]), key) for (key, ref) in totals.iteritems()]
kvp.sort()
kvp.reverse()

for (count, k) in kvp:
    uris = totals[k]
    if 1 == len(uris) and uris.keys()[0] == '-':
        pass
    else:
        print "      <dt>%s (%d)</dt>" % (k,count)
        print "      <dd>"
        print "        <ul>"
        for uri in sorted(uris.keys()):
            print '       <li>%4d <a href="%s">%s</a> </li>' % (uris[uri], escape(uri), escape(uri))
        print "        </ul>"
        print "      </dd>"

print """</dl>
</body>"""
