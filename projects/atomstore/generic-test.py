#!/usr/bin/python2.4
import generic
import unittest
import os
import sys
import libxml2
from StringIO import StringIO

def parseBody(body):
    body.seek(0)
    doc = libxml2.parseDoc(body.read())
    ctxt = doc.xpathNewContext()
    ctxt.xpathRegisterNs('ac', 'http://purl.org/atom/app#')
    return (doc, ctxt)

class TestGeneric(unittest.TestCase):
    def setUp(self):
        # clean up the data directory
        # make sure there are 5 files in there with
        # different time stamps

        generic.BLOCK_SIZE = 3
        generic.datadir = 'genericstatic'

        generic.dynamic = "http://bitworking.org/projects/pyapp/genericedit/"
        generic.static = "http://bitworking.org/projects/pyapp/genericstatic/"
        files = [filename for filename in os.listdir(generic.datadir) if os.path.isfile(os.path.join(generic.datadir, filename))]
        [os.unlink(os.path.join(generic.datadir, f)) for f in files]
        files = range(1,6)
        for filename in files:
            path = os.path.join(generic.datadir, str(filename)) + ".txt"
            f = file(path, "w")
            f.write("Hello World\n")
            f.close()
            os.utime(path, (1124133584, 1124133584+int(filename)))

    def test_filelist_to_atomcoll_single(self):
        body = generic.filelist_to_atomcoll([(1124133584,'fred.txt')], "")
        (doc, ctxt) = parseBody(body)
        self.assertEqual(1, len(ctxt.xpathEval("//ac:collection/ac:member")))
        self.assertEqual("fred.txt", ctxt.xpathEval("//ac:member/@title")[0].get_content())
        self.assertEqual("2005-08-15T15:19:44+05:00", ctxt.xpathEval("//ac:member/@updated")[0].get_content())
        self.assertEqual("", ctxt.xpathEval("//ac:collection/@next")[0].get_content())

    def test_filelist_to_atomcoll_multiple(self):
        body = generic.filelist_to_atomcoll([(1124133584,'fred.txt'), (1124133585,'barney.txt')], "http://example.org/next")
        (doc, ctxt) = parseBody(body)
        self.assertEqual(2, len(ctxt.xpathEval("//ac:collection/ac:member")))
        self.assertEqual("fred.txt", ctxt.xpathEval("//ac:member/@title")[0].get_content())
        self.assertEqual("barney.txt", ctxt.xpathEval("//ac:member/@title")[1].get_content())
        self.assertEqual("2005-08-15T15:19:44+05:00", ctxt.xpathEval("//ac:member/@updated")[0].get_content())
        self.assertEqual("2005-08-15T15:19:45+05:00", ctxt.xpathEval("//ac:member/@updated")[1].get_content())
        self.assertEqual("http://example.org/next", ctxt.xpathEval("//ac:collection/@next")[0].get_content())

    def testGetBasic(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/&block=0'
        os.environ['HTTP_RANGE'] = ''
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertEqual(headers['Content-Type'], "application/atomcoll+xml")
        self.assertEqual(headers['Accept-Ranges'], "updated")
        (doc, ctxt) = parseBody(body)

        # Only 3 member's are returned
        self.assertEqual(3, len(ctxt.xpathEval("//ac:collection/ac:member")))
        
        # The second member is 2.txt
        self.assertEqual("2.txt", ctxt.xpathEval("//ac:member/@title")[1].get_content())

        # We have the right  pointer to the 'next' document
        self.assertEqual('http://bitworking.org/projects/pyapp/genericedit/_/3', ctxt.xpathEval("//ac:collection/@next")[0].get_content())
        
    def testGetBasic2(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/&block=3'
        os.environ['HTTP_RANGE'] = ''
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertEqual(headers['Content-Type'], "application/atomcoll+xml")
        self.assertEqual(headers['Accept-Ranges'], "updated")
        (doc, ctxt) = parseBody(body)

        self.assertEqual(2, len(ctxt.xpathEval("//ac:collection/ac:member")))
        self.assertEqual('', ctxt.xpathEval("//ac:collection/@next")[0].get_content())

    def testRanges(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['HTTP_RANGE'] = 'updated=2005-08-15T15:19:45+05:00/2005-08-15T15:19:46+05:00'
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertEqual(headers['Content-Type'], "application/atomcoll+xml")
        self.assertEqual(headers['Vary'], "Range")
        (doc, ctxt) = parseBody(body)

        self.assertEqual(2, len(ctxt.xpathEval("//ac:collection/ac:member")))
        self.assertEqual('', ctxt.xpathEval("//ac:collection/@next")[0].get_content())

    def testNoneInRanges(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['HTTP_RANGE'] = 'updated=2005-08-15T15:19:45+04:00/2005-08-15T15:19:46+04:00'
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertEqual(headers['Vary'], "Range")
        (doc, ctxt) = parseBody(body)
        self.assertEqual(0, len(ctxt.xpathEval("//ac:collection/ac:member")))
        self.assertEqual('', ctxt.xpathEval("//ac:collection/@next")[0].get_content())

    def testAllInRanges(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['HTTP_RANGE'] = 'updated=2005-08-15T15:19:45+05:00/2005-08-15T15:19:49+05:00'
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertEqual(headers['Vary'], "Range")
        (doc, ctxt) = parseBody(body)
        self.assertEqual(5, len(ctxt.xpathEval("//ac:collection/ac:member")))
        self.assertEqual('', ctxt.xpathEval("//ac:collection/@next")[0].get_content())
 
    def testUnknownRangeUnit(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['HTTP_RANGE'] = 'znarfbits=3-7,9-123'
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertFalse(headers.has_key('Vary'))
        self.assertEqual(headers['Accept-Ranges'], "updated")
        (doc, ctxt) = parseBody(body)
        self.assertEqual(3, len(ctxt.xpathEval("//ac:collection/ac:member")))
        self.assertEqual('http://bitworking.org/projects/pyapp/genericedit/_/3', ctxt.xpathEval("//ac:collection/@next")[0].get_content())

    def testInvalidRangeUnit(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['HTTP_RANGE'] = 'updated=3-7,9-123'
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "500 Internal Server Error")
        self.assertFalse(headers.has_key('Vary'))
 
    def testCreateNewMember(self):
        os.environ['REQUEST_METHOD'] = 'POST'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['CONTENT_TYPE'] = 'text/plain'
        sys.stdin = StringIO("Hi Planet!") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "201 Created")
        self.assertTrue(headers.has_key('Location'))
        (doc, ctxt) = parseBody(body)

    def testCreateWithName(self):
        os.environ['REQUEST_METHOD'] = 'POST'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['CONTENT_TYPE'] = 'text/plain'
        os.environ['HTTP_NAME'] = 'fred.txt'
        sys.stdin = StringIO("Hi Planet!") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "201 Created")
        self.assertTrue(headers.has_key('Location'))
        (doc, ctxt) = parseBody(body)
        self.assertEqual("fred.txt", ctxt.xpathEval("//ac:member/@title")[0].get_content())
        self.assertEqual(generic.static + "fred.txt", ctxt.xpathEval("//ac:member/@hrefreadonly")[0].get_content())
        self.assertEqual(generic.dynamic + "fred.txt", ctxt.xpathEval("//ac:member/@href")[0].get_content())

    def testCreateWithMismatchedExt(self):
        os.environ['REQUEST_METHOD'] = 'POST'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['CONTENT_TYPE'] = 'text/plain'
        os.environ['HTTP_NAME'] = 'fred.py'
        sys.stdin = StringIO("Hi Planet!") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "201 Created")
        self.assertTrue(headers.has_key('Location'))
        (doc, ctxt) = parseBody(body)
        self.assertEqual("fred.py.asc", ctxt.xpathEval("//ac:member/@title")[0].get_content())

    def testCreateNoLeadingDot(self):
        os.environ['REQUEST_METHOD'] = 'POST'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['CONTENT_TYPE'] = 'text/plain'
        os.environ['HTTP_NAME'] = '.fred.txt'
        sys.stdin = StringIO("Hi Planet!") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "201 Created")
        self.assertTrue(headers.has_key('Location'))
        (doc, ctxt) = parseBody(body)
        self.assertEqual("fred.txt", ctxt.xpathEval("//ac:member/@title")[0].get_content())

    def testCreateNoDirSymbols(self):
        os.environ['REQUEST_METHOD'] = 'POST'
        os.environ['QUERY_STRING'] = 'path=/'
        os.environ['CONTENT_TYPE'] = 'text/plain'
        os.environ['HTTP_NAME'] = '.fred/../.htaccess'
        sys.stdin = StringIO("Hi Planet!") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "201 Created")
        self.assertTrue(headers.has_key('Location'))
        (doc, ctxt) = parseBody(body)
        self.assertEqual("fred...htaccess.asc", ctxt.xpathEval("//ac:member/@title")[0].get_content())



class TestGenericMember(unittest.TestCase):
    def setUp(self):
        # clean up the data directory
        # make sure there are 5 files in there with
        # different time stamps

        generic.BLOCK_SIZE = 3
        generic.datadir = 'genericstatic'

        generic.dynamic = "http://bitworking.org/projects/pyapp/genericedit/"
        generic.static = "http://bitworking.org/projects/pyapp/genericstatic/"
        files = [filename for filename in os.listdir(generic.datadir) if os.path.isfile(os.path.join(generic.datadir, filename))]
        [os.unlink(os.path.join(generic.datadir, f)) for f in files]
        files = range(1,6)
        for filename in files:
            path = os.path.join(generic.datadir, str(filename)) + ".txt"
            f = file(path, "w")
            f.write("Hello World\n")
            f.close()
            os.utime(path, (1124133584, 1124133584+int(filename)))
        f = file(os.path.join(generic.datadir, ".htaccess"), "w")
        f.write("")
        f.close()

    def testDelete(self):
        os.environ['REQUEST_METHOD'] = 'DELETE'
        os.environ['QUERY_STRING'] = 'path=/2.txt'
        sys.stdin = StringIO("Hi Planet!") 
        fullpath = os.path.join(generic.datadir, '2.txt')
        self.assert_(os.path.exists(fullpath))
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertFalse(os.path.exists(fullpath))

    def testDeleteHtAcess(self):
        os.environ['REQUEST_METHOD'] = 'DELETE'
        os.environ['QUERY_STRING'] = 'path=/.htaccess'
        sys.stdin = StringIO("Hi Planet!") 
        fullpath = os.path.join(generic.datadir, '.htaccess')
        self.assert_(os.path.exists(fullpath))
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "403 Forbidden")
        self.assert_(os.path.exists(fullpath))

    def testDeleteNonExistent(self):
        os.environ['REQUEST_METHOD'] = 'DELETE'
        os.environ['QUERY_STRING'] = 'path=//fred.txt'
        sys.stdin = StringIO("Hi Planet!") 
        fullpath = os.path.join(generic.datadir, '.htaccess')
        self.assert_(os.path.exists(fullpath))
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "403 Forbidden")
        self.assert_(os.path.exists(fullpath))

    def testGet(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/3.txt'
        sys.stdin = StringIO("") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertEqual(headers['Content-Type'], "text/plain")
        self.assertEqual(body.read(), "Hello World\n")

    def testGetForbidden(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=//3.txt'
        sys.stdin = StringIO("") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "403 Forbidden")
        self.assertEqual(headers['Content-Type'], "text/plain")

    def testGetHtAccess(self):
        os.environ['REQUEST_METHOD'] = 'GET'
        os.environ['QUERY_STRING'] = 'path=/.htaccess'
        sys.stdin = StringIO("") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "403 Forbidden")
        self.assertEqual(headers['Content-Type'], "text/plain")


    def testPut(self):
        os.environ['REQUEST_METHOD'] = 'PUT'
        os.environ['QUERY_STRING'] = 'path=/3.txt'
        sys.stdin = StringIO("This is a replacement.") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "200 Ok")
        self.assertEqual(headers['Content-Type'], "text/plain")
        fullpath = os.path.join(generic.datadir, '3.txt')
        f = file(fullpath, "r")
        self.assertEqual(f.read(), "This is a replacement.")
        f.close()


    def testPutForbidden(self):
        os.environ['REQUEST_METHOD'] = 'PUT'
        os.environ['QUERY_STRING'] = 'path=//3.txt'
        sys.stdin = StringIO("") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "403 Forbidden")
        self.assertEqual(headers['Content-Type'], "text/plain")
        fullpath = os.path.join(generic.datadir, '3.txt')
        f = file(fullpath, "r")
        self.assertEqual(f.read(), "Hello World\n")
        f.close()


    def testPutHtAccess(self):
        os.environ['REQUEST_METHOD'] = 'PUT'
        os.environ['QUERY_STRING'] = 'path=/.htaccess'
        sys.stdin = StringIO("") 
        (headers, body) = generic.GenericMain()
        self.assertEqual(headers['Status'], "403 Forbidden")
        self.assertEqual(headers['Content-Type'], "text/plain")
        fullpath = os.path.join(generic.datadir, '3.txt')
        f = file(fullpath, "r")
        self.assertEqual(f.read(), "Hello World\n")
        f.close()











if __name__ == "__main__":
    unittest.main()

