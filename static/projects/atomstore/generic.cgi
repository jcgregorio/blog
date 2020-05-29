#!/usr/bin/python2.4

__author__ = "Joe Gregorio <http://bitworking.org/>"
__version__ = "Revision: 1.00"
__copyright__ = "Copyright (c) 2005 Joe Gregorio"
__license__ = "MIT"

sys.path.extend(['/home/jcgregorio/lib/python2.4/site-packages/','/home/jcgregorio/lib/python2.4/'])
import atomstore
import os
import cgi
from StringIO import StringIO

DBNAME = 'livestore'

if not os.path.dirname(DBNAME):
    store.create(DBNAME, "joe@bitworking.org")

store = atomstore.Store(DBNAME)

method = os.environ.get("REQUEST_METHOD", "GET")
method = method == 'HEAD' and 'GET' or method
params = cgi.parse_qs(os.environ.get('QUERY_STRING', 'id=some-id'))


# local path to the static data
datadir = "static"

# HTTP Address of the collection
dynamic = "http://bitworking.org/projects/pyapp/edit/"

# HTTP Address of the statics
# Where the generic (pictures, pdfs, etc) are stored.
static = "http://bitworking.org/projects/pyapp/static/"


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
            try:
                returnValue = getattr(self, fun_name)(params)
            except Exception, e:
                returnValue = self.exception(method, e, params)
        else:
            returnValue = self.nomatch(method, mime_type)
        return returnValue

class GenericCollection(SimpleHttpDispatch):
    def POST(self, params):
        # Create a new member of the collection.
        # This is a two step process, pick the content type and the file name
        name = '' 
        ext = ''
        if os.environ.has_key('HTTP_NAME'):
            # Using either the Name: header (after making it safe)
            from urllib import unquote
            name = unquote(os.environ['HTTP_NAME']).encode('us-ascii', 'ignore')
            name = re.sub("\/", "", name)
            name = re.sub("^\.*", "", name)
            (name, provided_ext) = os.path.splitext(name)
            # Determine if it has a valid file extension.
            if mime.mime_type(provided_ext[1:]):
                ext = provided_ext[1:]
            else:
                name = name + provided_ext

        if not name: 
            # generate a random one.
            import random
            name = "".join(["abcdefghijklmnopqrstuvwxyz"[random.randint(0,25)] for c in range(20)])
       
        if not ext:
            # generate an extension from the content-type.
            ext = mime.extension(os.environ.get('CONTENT_TYPE', ''))

        if not ext:
            return ({"Status": "400 Bad Request", 
                "Content-Type": "text/plain"},
                StringIO("A Content-Type or a valid file extension MUST be supplied."))
        name = name + "." + ext
          
        filename = os.path.join(datadir, name)
        f = open(filename, "wb")
        f.write(sys.stdin.read())
        f.close()

        returnHeaders = {"Status": "201 Created", 
            "Content-Type": "application/atomcoll+xml",
            "Location": static + name 
        }

        body = filelist_to_atomcoll([(os.stat(filename)[ST_MTIME], name)], "")
        return (returnHeaders, body)
         


    def _get_range(self, range_begin, range_end):
        def f(filenames_member):
            date = local_to_datetime(filenames_member[1][0])
            return date >= range_begin and date <= range_end
        return f


    def GET(self, params):
        returnHeaders = {"Status": "200 Ok", 
            "Content-Type": "application/atomcoll+xml",
            "Accept-Ranges": "updated"
        }
           
        static_dir = os.path.join(datadir, params['path'][0][1:])
        dated_files = [(os.stat(os.path.join(static_dir, filename))[ST_MTIME], filename) for filename in os.listdir(static_dir) if os.path.isfile(os.path.join(static_dir, filename))]
        dated_files.sort()
        filenames = zip(range(len(dated_files)), dated_files) 
        # 'filenames' is now a sorted list of tuples, (index, (time, filename)) for each file.
        next_attr = ""

        http_range = os.environ.get('HTTP_RANGE', '')
        if http_range.split("=")[0].strip() == "updated":
            (range_type, begin_end) = http_range.split("=")
            (date_begin_iso, date_end_iso) = begin_end.split('/')
            date_begin = iso_to_datetime(date_begin_iso)
            date_end = iso_to_datetime(date_end_iso)
            filenames = filter(self._get_range(date_begin, date_end), filenames)
            returnHeaders['Vary'] = 'Range'
        else:
            begin = 0
            end   = BLOCK_SIZE
            len_filenames = len(filenames)
            next_subset = BLOCK_SIZE 
            next_attr = ""

            if params.has_key('block'):
                begin = int(params['block'][0])
                assert begin >= 0
                next_subset = begin + BLOCK_SIZE
                end = begin + BLOCK_SIZE

            if begin > len_filenames:
                raise RuntimeError, "The range of members selected is invalid."
            if end >= len_filenames:
                next_subset = -1
                end = len_filenames
            filenames = filenames[begin:end]
            if next_subset >= 0:
                next_attr = dynamic + "_/" + params['path'][0][1:] + str(next_subset)
        filenames = [fileinfo for (index, fileinfo) in filenames]
        body = filelist_to_atomcoll(filenames, next_attr)

        return (returnHeaders, body) 
    

class GenericCollectionMember(SimpleHttpDispatch):

    def _apply_if_valid(self, params, f):
        name = params['path'][0][1:]
        if re.match("^\.+", name):
            return ({"Status": "403 Forbidden", 
                "Content-Type": "text/plain"},
                StringIO("Forbidded. Files beginning with '.' can not be edited."))
        full_filename = os.path.abspath(os.path.join(datadir, name))
        if is_proper_subdir(datadir, full_filename):
            if os.path.exists(full_filename):
                return f(full_filename)
        else:
            return ({"Status": "403 Forbidden", 
                "Content-Type": "text/plain"},
                StringIO("Forbidded. Invalid relative directory given."))

    def _PUT(self, full_filename):
        f = file(full_filename, "w")
        f.write(sys.stdin.read())
        f.close()
        # Could also return a 204 with updated ETag and Last Modifed headers
        return ({"Status": "200 Ok", 
            "Content-Type": "text/plain"},
            StringIO(""))
 
   
    def PUT(self, params):
        # Add checks for Content-* headers we don't understand
        return self._apply_if_valid(params, self._PUT)

    def _DELETE(self, full_filename):
        os.unlink(full_filename)
        return ({"Status": "200 Ok", 
            "Content-Type": "text/plain"},
            StringIO(""))
 
    def DELETE(self, params):
        return self._apply_if_valid(params, self._DELETE)

    def _GET(self, full_filename):
        f = file(full_filename, "r")
        # Could also return a 204 with updated ETag and Last Modifed headers
        (name, provided_ext) = os.path.splitext(full_filename)
        mime_type = mime.mime_type(provided_ext[1:])
        return ({"Status": "200 Ok", 
            "Content-Type": mime_type},
            f)

    def GET(self, params):
        return self._apply_if_valid(params, self._GET)

def GenericMain():
    method = os.environ.get("REQUEST_METHOD", "GET")
    method = method == 'HEAD' and 'GET' or method
    params = cgi.parse_qs(os.environ.get('QUERY_STRING', ''))
    if params.has_key('id'): 
        return  CollectionMember().dispatch(method, params)
    elif len(path_info):
        return  Collection().dispatch(method, params)
    else:
        return SimpleHttpDispatch().nomatch(method, params)
    
if __name__ == "__main__":
    (headers, body) = GenericMain()

    f = open("log", "w")
    f.write("\n".join(["%040s = %s" % (name, value) for (name, value) in os.environ.iteritems()]))
    f.close()

    sys.stdout.write("\n".join(["%s: %s" % (key, value) for (key, value) in headers.iteritems()]))
    sys.stdout.write("\n\n") 
    sys.stdout.write(body.read())
