import re, os, mimeparse
from StringIO import StringIO

__author__ = "Joe Gregorio <http://bitworking.org/>"
__version__ = "Revision: 2.00"
__copyright__ = "Copyright (c) 2005 Joe Gregorio"
__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

class BaseHttpDispatch:
    """Dispatch HTTP events based on the method and requested mime-type"""
    def __init__(self, mime_types_supported = {}):
        """mime_types_supported is a dictionary that maps
           supported mime-type names to the shortened names that are used in 
           dispatching.
        """
        self.mime_types_supported = mime_types_supported

    def nomatch(self, method, mime_type):
        """This is the default handler called if
           there is no match found. Overload to add
           your own behaviour."""
        return ({"Status": "404 Not Found", "Content-type": "text/plain"}, 
                StringIO("The requested URL was not found on this server.")) 

    def exception(self, method, mime_type, exception):
        """This is the default handler called if an
        exception occurs while processing."""
        return ({"Status": "500 Internal Server Error", 
                "Content-type": "text/plain"}, 
                StringIO("The server encountered an unexpected condition\
                        which prevented it from fulfilling the request." + str(exception))) 

    def _call_fn(self, fun_name, method, mime_type):
        try:
            return getattr(self, fun_name)()
        except Exception, e:
            return self.exception(method, mime_type, e)


    def dispatch(self, method, mime_type):
    	"""Pass in the method and the media-range and the best matching 
        function will be called. For example, if BaseHttpDispatch is 
        constructed with a mime type map
        that maps 'text/xml' to 'xml', then if dispatch is called with
    	'POST' and 'text/xml' will first look for 'POST_xml' and 
        then if that fails it will try to call 'POST'. 
        
        Each function so defined must return a tuple
        (headers, body) 
        
        where 'headers' is a dictionary of headers for the response
        and 'body' is any object that simulates a file. 
        """

        returnValue = ({}, StringIO(""))
        if mime_type and self.mime_types_supported:
            match = mimeparse.best_match(self.mime_types_supported.keys(), mime_type)
            mime_type_short_name = self.mime_types_supported.get(match , '')
        else:
            mime_type_short_name = ""
        fun_name = method + "_" + mime_type_short_name
        if fun_name in dir(self) and callable(getattr(self, fun_name)):
            returnValue = self._call_fn(fun_name, method, mime_type)
        elif method in dir(self) and callable(getattr(self, method)):
            returnValue = self._call_fn(method, method, mime_type)
        else:
            returnValue = self.nomatch(method, mime_type)
        return returnValue






if __name__ == "__main__":
    import unittest

    class MethodDispatch(BaseHttpDispatch):
        def __init__(self):
            BaseHttpDispatch.__init__(self, {})
            self.last_method = ''
        def POST(self):
            self.last_method = 'post'
        def GET(self):
            self.last_method = 'get'

    class MethodAndTypeDispatch(BaseHttpDispatch):
        def __init__(self):
            BaseHttpDispatch.__init__(self, {'application/xml':'xml', 'application/html':'html'})
            self.last_method = ''
        def POST(self):
            self.last_method = 'post'
        def GET(self):
            self.last_method = 'get'
        def GET_xml(self):
            self.last_method = 'get_xml'
        def GET_html(self):
            self.last_method = 'get_html'

    class MethodAndTypeWildcard(BaseHttpDispatch):
        def __init__(self):
            BaseHttpDispatch.__init__(self, {'image/*':'image', 'application/html':'html'})
            self.last_method = ''
        def POST(self):
            self.last_method = 'post'
        def GET(self):
            self.last_method = 'get'
        def GET_image(self):
            self.last_method = 'get_image'
        def GET_html(self):
            self.last_method = 'get_html'

    class ErrorConditions(BaseHttpDispatch):
        def __init__(self):
            BaseHttpDispatch.__init__(self, {'image/*':'image', 'application/html':'html'})
            self.last_method = ''
        def POST(self):
            self.last_method = 'post'

        def nomatch(self, method, mime_type):
            self.last_method = 'nomatch'
            pass

        def exception(self, method, mime_type, exception):
            self.last_method = 'exception:' + str(exception)

        def GET_html(self):
            raise Exception, "Just pretending"



    class TestDispatchingMethod(unittest.TestCase):
        def test_method_only(self):
            dispatcher = MethodDispatch()

            dispatcher.dispatch('GET', 'html')
            self.assertEqual('get', dispatcher.last_method)

            dispatcher.dispatch('POST', 'html')
            self.assertEqual('post', dispatcher.last_method)

            dispatcher.last_method = ''
            dispatcher.dispatch('PUT', 'html')
            self.assertEqual('', dispatcher.last_method)

        def test_method_and_type(self):
            dispatcher = MethodAndTypeDispatch()

            dispatcher.dispatch('GET', '')
            self.assertEqual('get', dispatcher.last_method)

            dispatcher.dispatch('GET', 'application/html')
            self.assertEqual('get_html', dispatcher.last_method)

            dispatcher.dispatch('GET', 'application/xml')
            self.assertEqual('get_xml', dispatcher.last_method)

            dispatcher.dispatch('GET', 'application/xhtml')
            self.assertEqual('get', dispatcher.last_method)

            dispatcher.dispatch('GET', 'application/*')
            self.assertEqual('get_xml', dispatcher.last_method)

            dispatcher.dispatch('GET', 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5')
            self.assertEqual('get_xml', dispatcher.last_method)

        def test_method_and_wildcard_type(self):
            dispatcher = MethodAndTypeWildcard()

            dispatcher.dispatch('GET', '')
            self.assertEqual('get', dispatcher.last_method)

            dispatcher.dispatch('GET', 'image/*')
            self.assertEqual('get_image', dispatcher.last_method)

            dispatcher.dispatch('GET', '*/*')
            self.assertEqual('get_image', dispatcher.last_method)

            dispatcher.dispatch('GET', 'image/png')
            self.assertEqual('get_image', dispatcher.last_method)

        def test_errors(self):
            dispatcher = ErrorConditions()

            dispatcher.dispatch('GET', '')
            self.assertEqual('nomatch', dispatcher.last_method)

            dispatcher.dispatch('POST', 'image/*')
            self.assertEqual('post', dispatcher.last_method)

            dispatcher.dispatch('GET', 'application/html')
            self.assertEqual('exception:Just pretending', dispatcher.last_method)

    unittest.main()


