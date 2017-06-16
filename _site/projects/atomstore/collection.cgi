#!/usr/bin/python2.4

__author__ = "Joe Gregorio <http://bitworking.org/>"
__version__ = "$Revision: 180 $"
__copyright__ = "Copyright (c) 2006 Joe Gregorio"
__license__ = "MIT"

import cgitb; cgitb.enable()

import sys
sys.path.extend(['/home/jcgregorio/lib/python2.4/site-packages/','/home/jcgregorio/lib/python2.4/'])

import atomstore
import os
import cgi
from StringIO import StringIO
import kid
import md5
import mimeparse

DBNAME = 'livestore'

# The Atom Validity checking could probably be moved 
# into the atom store itself.
STRICT = True

f = open("log", "a")

if STRICT:
    import feedvalidator
    from feedvalidator import compatibility
    from gettext import gettext as _
    import cStringIO

    def validate_atom(content, baseuri):
        try:
            events = feedvalidator.validateStream(cStringIO.StringIO(content), firstOccurrenceOnly=1,base=baseuri)['loggedEvents']
        except feedvalidator.logging.ValidationFailure, vf:
            events = [vf.event]

        filterFunc = getattr(compatibility, "AA")
        events = filterFunc(events)
        if len(events):
            from feedvalidator.formatter.text_plain import Formatter
            output = Formatter(events)
            return "\n".join(output)
        else:
            return ""



if not os.path.isdir(DBNAME):
    atomstore.create(DBNAME, "joe@bitworking.org", "collection.cgi?id=%s")

store = atomstore.Store(DBNAME)

method = os.environ.get("REQUEST_METHOD", "GET")
method = method == 'HEAD' and 'GET' or method
params = cgi.parse_qs(os.environ.get('QUERY_STRING', 'id=some-id'))


class SimpleHttpDispatch:
    """Dispatch HTTP events based on the method."""

    def nomatch(self, method, params):
        """This is the default handler called if
           there is no match found. Overload to add
           your own behaviour.
        """
        return ({"Status": "404 Not Found", "Content-Type": "text/plain"}, 
                StringIO("The requested URL was not found on this server.")
                ) 

    def exception(self, method, exception, params):
        """This is the default handler called if an
        exception occurs while processing."""
        return ({"Status": "500 Internal Server Error", 
                "Content-Type": "text/plain"}, 
                StringIO("The server encountered an unexpected condition\
                        which prevented it from fulfilling the request." + str(exception))) 

    def _conditional_get(self, headerbody):
        (headers, body) = headerbody
        if not headers.has_key('ETag'):
            body_str = body.read()
            body.seek(0)
            headers['ETag'] = '"%s"' % md5.new(body_str).hexdigest()
        incoming_etag = os.environ.get('HTTP_IF_NONE_MATCH', '')
        if incoming_etag == headers['ETag']:
            headers['Status'] = '304 Not Modified' 
            body = StringIO("")
        return (headers, body) 

    def dispatch(self, method, params):
    	"""Pass in the method and the best matching 
        function will be called. 
        
        Each function so defined must return a tuple

           (headers, body) 
        
        where 'headers' is a dictionary of headers for the response
        and 'body' is any object that simulates a file. 
        """

        returnValue = ({}, StringIO(""))
        fun_name = method 
        if fun_name in dir(self) and callable(getattr(self, fun_name)):
            #try:
            returnValue = getattr(self, fun_name)(params)
            #except Exception, e:
            #    returnValue = self.exception(method, e, params)
        else:
            returnValue = self.nomatch(method, mime_type)
        if method == "GET":
            returnValue = self._conditional_get(returnValue)
        return returnValue

class Collection(SimpleHttpDispatch):
    def POST(self, params):
        content_type = os.environ.get('CONTENT_TYPE', '')
        if content_type:
            mtype = mimeparse.parse_mime_type(content_type)
        else:
            mtype = None
        if not mtype or not ((mtype[0] == 'application') and (mtype[1] == 'atom+xml')):
            return ({"Status": "400 Bad Request", "Content-Type": "text/plain"}, StringIO("Wrong media type:" + str(os.environ)))

        content = sys.stdin.read()
        if STRICT:
            errs = validate_atom(content, os.environ['REQUEST_URI'])
            if errs:
                return ({"Status": "400 Bad Request", "Content-Type": "text/plain"}, StringIO("Invalid Atom: " + errs))
        id = store.post(content)

        returnHeaders = {
            "Status": "201 Created", 
            "Location": os.environ['REQUEST_URI'] + "?id=" + id
        }

        body = StringIO("")
        return (returnHeaders, body)
         
    def GET(self, params):
        returnHeaders = {
            "Status": "200 Ok", 
            "Content-Type": "application/atom+xml",
            "Cache-Control": "must-revalidate, max-age=0",
        }
        length = 20
        offset = 0
        nextrange = None
        if params.has_key('index'):
            offset = int(params['index'])
        

        selected_entries = [dict(
                title = i[1], 
                id = store.id_to_uri_id(i[0]), 
                edituri = store.id_to_edit_uri(i[0]),
                updated = store.time_to_datestring(i[2]) 
                ) for i in store.index(length, offset)]

        if len(selected_entries) == 20:
            nextrange = offset + 20  

        list_doc = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:py="http://purl.org/kid/ns#">
  <updated>2003-12-13T18:30:02Z</updated>
  <author> 
     <name>Joe Gregorio</name>
  </author> 
  <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
  <link rel="self" href="http://${host}${script_name}"/>

  <link py:if="nextrange" rel="next" href="${script_name}?index=${nextrange}"/>

  <entry py:for="e in entries" >
      <title type="text">${e['title']}</title>
      <id>${e['id']}</id>
      <link rel="edit" href="${e['edituri']}"/>
      <updated>${e['updated']}</updated>
      <content type="text">Non blank content element filler.</content>
  </entry>

</feed>"""


        template = kid.Template(source=list_doc, entries=selected_entries, script_name=os.environ['SCRIPT_NAME'], host=os.environ['HTTP_HOST'], nextrange = nextrange)
        body = StringIO(template.serialize())

        return (returnHeaders, body) 
   
class Introspection(SimpleHttpDispatch):

    def GET(self, params):
        returnHeaders = {
            "Status": "200 Ok", 
            "Content-Type": "application/atomcoll+xml",
        }
        coll = """<?xml version="1.0" encoding='utf-8'?>
<service xmlns="http://purl.org/atom/app#">
  <workspace title="My Blog Entries">
    <collection xmlns="http://purl.org/atom/app#" title="My Blog Entries" href="http://${host}${script_name}"> 
        <member-type>entry</member-type>
    </collection>
  </workspace>
</service>"""

        template = kid.Template(source=coll, script_name=os.environ['SCRIPT_NAME'], host=os.environ['HTTP_HOST'] , index = '{index}')
        body = StringIO(template.serialize())

        return (returnHeaders, body) 

class CollectionMember(SimpleHttpDispatch):

    def GET(self, params):
        try:
            return ({"Status": "200 Ok", 
                "Content-Type": "application/atom+xml"},
                StringIO(store.get(params['id'][0])))
        except:
            return ({"Status": "404 Not Found", 
                "Content-Type": "text/plain"},
                StringIO("Not Found"))

    def PUT(self, params):

        content = sys.stdin.read()
        if STRICT:
            errs = validate_atom(content, os.environ['REQUEST_URI'])
            if errs:
                return ({"Status": "400 Bad Request", "Content-Type": "text/plain"}, StringIO("Invalid Atom: " + errs))
        store.put(params['id'][0], content) 
        return ({"Status": "200 Ok"}, StringIO(""))

    def DELETE(self, params):
        store.delete(params['id'][0])
        return ({"Status": "200 Ok"},
            StringIO(""))


def GenericMain():
    method = os.environ.get("REQUEST_METHOD", "GET")
    method = method == 'HEAD' and 'GET' or method
    params = cgi.parse_qs(os.environ.get('QUERY_STRING', ''))
    if params.has_key('id'): 
        return  CollectionMember().dispatch(method, params)
    elif params.has_key('introspection'): 
        return  Introspection().dispatch(method, params)
    else:
        return  Collection().dispatch(method, params)
    
(headers, body) = GenericMain()

f.write("\n\nRequest\n")
f.write("\n".join(["%040s = %s" % (name, value) for (name, value) in os.environ.iteritems()]))
f.write("\n\nResponse\n")
f.write("\n".join(["%040s = %s" % (key, value) for (key, value) in headers.iteritems()]))
f.write(body.getvalue())
f.close()

sys.stdout.write("\n".join(["%s: %s" % (key, value) for (key, value) in headers.iteritems()]))
sys.stdout.write("\n\n") 
sys.stdout.write(body.read())


