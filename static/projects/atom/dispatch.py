import re, os

__author__ = "Joe Gregorio <http://bitworking.org/>"
__version__ = "Revision: 1.00"
__copyright__ = "Copyright (c) 2002 Joe Gregorio"
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

def fileNotFound():
	print "Status: 404 Not Found\nContent-type: text/html\n"
	print "<html><body><h1>File Not Found</h1></body></html>\n"

def returnFileAsContent(filename, mime_type):
	"""Return the given file if possible, including all the
	right headers, or return a 404 if it can't be found."""
	if os.access(filename, os.F_OK):
		print "Content-type: " + mime_type + "\n"
		f = file(filename, "rb")
		s = f.read()
		print s
		f.close()
	else:
		fileNotFound()

def stripSlashes(pathInfo):
	"""Strip leading and trailing slashes from a string, if they exist"""
	pathInfo = re.sub("^/", "", pathInfo)
	pathInfo = re.sub("/$", "", pathInfo)
	return pathInfo

class BaseHttpDispatch:
	"""Dispatch HTTP events based on the verb and requested Mimi-Type"""
	def dispatch(self, verb, mime_type):
		"""Pass in the verb and the simplified mime-type, i.e. html or xml, 
		and the best matching function will be called, for example
		'POST' and 'xml' will first look for 'POST_xml' and then if that fails
		it will try to call 'POST'. Returns True if any match was found."""
		returnValue = False
		fun_name = verb + "_" + mime_type
		if fun_name in dir(self) and callable(getattr(self, fun_name)):
			getattr(self, fun_name)()
			returnValue = True
		elif verb in dir(self) and callable(getattr(self, verb)):
			getattr(self, verb)()
			returnValue = True
		return returnValue


		
		

	








