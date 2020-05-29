#!/home/jcgregorio/bin/python2.5
import cgitb; cgitb.enable()
import StringIO
import os
import sys
from wsgiref.handlers import BaseCGIHandler
from dispatcher import app 
import logging

try:
    f = StringIO.StringIO("")
    os.environ['PATH_INFO'] = os.environ.get('PATH_INFO', '/')
    if "HEAD" == os.environ['REQUEST_METHOD']:
        os.environ['REQUEST_METHOD'] = "GET"
    BaseCGIHandler(sys.stdin, sys.stdout, f, os.environ).run(app)
    errors = f.getvalue()
    if errors:
        logging.error(errors)
except:
    import sys
    import traceback
    logging.error(traceback.format_tb(sys.exc_info()[2]))
    logging.error(repr(os.environ))
    


