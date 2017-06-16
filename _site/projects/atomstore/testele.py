
import StringIO

from elementtree.ElementTree import ElementTree, SubElement, XML, tostring

content = """<?xml version="1.0" encoding="utf-8"?>
   <feed xmlns="http://www.w3.org/2005/Atom"
    xml:lang="en">

     <title type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">Example <b>Feed</b></div></title>
     <link href="http://example.org/"/>
     <updated>2003-12-13T18:30:02Z</updated>
     <author>
       <name>John Doe</name>
     </author>
     <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>

     <entry>
       <title type="xhtml">Atom-Powered <br/> Robots Run Amok</title>
       <link href="http://example.org/2003/12/13/atom03"/>
       <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
       <updated>2003-12-13T18:30:02Z</updated>
       <summary>Some text.</summary>
     </entry>

   </feed>"""

etree = ElementTree(file=StringIO.StringIO(content))
feed = XML(content)

print etree
print feed

#print len(feed)
#print feed[0]
#print feed.keys()

ATOM = "http://www.w3.org/2005/Atom"

entry = etree.getiterator('{%s}entry'%ATOM)[0]
new_lin = SubElement(entry, '{%s}link'%ATOM)
new_lin.set('rel', 'source')
new_lin.set('href', 'http://somthing.org')

title = etree.findall('{%s}title'%ATOM)[0]
print tostring(title)

missing = etree.findall('{%s}missing'%ATOM)
print missing

for e in etree.findall('//{%s}link'%ATOM):
    print e.get('rel', 'alternate')

s = StringIO.StringIO()
etree.write(s)
s.seek(0)
print s.getvalue()
