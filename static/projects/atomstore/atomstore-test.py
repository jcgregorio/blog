#!/usr/bin/python2.4
import atomstore
import unittest
import os
import sys
import libxml2
import glob
import time
import random
import threading
from cStringIO import StringIO

DBDIR = 'db'

BASIC_ENTRY = """<?xml version="1.0" encoding="utf-8"?>
  <entry xmlns="http://www.w3.org/2005/Atom">
    <title>Atom-Powered Robots Run Amok</title>
    <link href="http://example.org/2003/12/13/atom03"/>
    <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
    <updated>2003-12-13T18:30:02Z</updated>
    <summary>Some text.</summary>
  </entry>
"""

UNICODE_ENTRY = u"""<entry xmlns="http://www.w3.org/2005/Atom">
    <title>Atom-Powered Robots Run Amok</title>
    <link href="http://example.org/2003/12/13/atom03"/>
    <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
    <updated>2003-12-13T18:30:02Z</updated>
    <published>2003-12-13T08:29:29-04:00</published>
    <summary>Some text.</summary>
   <content type="xhtml" xml:lang="en" 
     xml:base="http://bitworking.org/">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p><i>Let's get publishing: \N{WHITE CHESS KING}</i></p>
      </div>
    </content>
  </entry>
"""

BASIC_TEMPLATE = """<entry xmlns="http://www.w3.org/2005/Atom">
    <title>%s</title>
    <link rel="alternate" type="text/html" 
     href="http://example.org/2005/04/02/atom"/>
    <link rel="enclosure" type="audio/mpeg" length="1337"
     href="http://example.org/audio/ph34r_my_podcast.mp3"/>
    <id>tag:example.org,2003:3.2397</id>
    <updated>2005-07-10T12:29:29Z</updated>
    <published>2003-12-13T08:29:29-04:00</published>
    <author>
      <name>Mark Pilgrim</name>
      <uri>http://example.org/</uri>
      <email>f8dy@example.com</email>
    </author>
    <contributor>
      <name>Sam Ruby</name>
    </contributor>
    <contributor>
      <name>Joe Gregorio</name>
    </contributor>
    <content type="xhtml" xml:lang="en" 
     xml:base="http://diveintomark.org/">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p><i>[Update: The Atom draft is finished.]</i></p>
      </div>
    </content>
  </entry>"""

MINIMUM_ENTRY = """<entry xmlns="http://www.w3.org/2005/Atom">
    <title></title>
    <id></id>
    <updated>2003-12-13T18:30:02Z</updated>
    <author>
      <name>Joe Gregorio</name>
    </author>
    <content type="text">Some text.</content>
  </entry>
"""

MISSING_ID_ENTRY = """<entry xmlns="http://www.w3.org/2005/Atom">
    <title></title>
    <updated>2003-12-13T18:30:02Z</updated>
    <author>
      <name>Joe Gregorio</name>
    </author>
    <content type="text">Some text.</content>
  </entry>
"""

MISSING_TITLE_ENTRY = """<entry xmlns="http://www.w3.org/2005/Atom">
    <id/>
    <updated>2003-12-13T18:30:02Z</updated>
    <author>
      <name>Joe Gregorio</name>
    </author>
    <content type="text">Some text.</content>
  </entry>
"""

NOT_WELL_FORMED_ENTRY = """<entry xmlns="http://www.w3.org/2005/Atom">
    <id/>
    <updated>2003-12-13T18:30:02Z</updated>
    <author>
      <name>Joe Gregorio</name>
    </author>
    <content type="text">Some text.</content>
  </entry
"""

CATEGORY_ENTRY = """<entry xmlns="http://www.w3.org/2005/Atom">
    <title></title>
    <id></id>
    <updated>2003-12-13T18:30:02Z</updated>
    <author>
      <name>Joe Gregorio</name>
    </author>
    <content type="text">Some text.</content>
    <category term="%s" scheme="http://technorati.com/tag/">REST</category>
    <category term="%s" scheme="http://technorati.com/tag/">Atom Publishing Protocol</category>
  </entry>
"""

only_xhtml_filter = """
ATOM = "http://www.w3.org/2005/Atom"
ATOM_CONTENT = '{%s}content' % ATOM

def check(entry):
    content = entry.findall(ATOM_CONTENT)
    if 0 == len(content) or (1 == len(content) and content[0].get('type', '') == 'xhtml'):
        return entry
    else:
        return None
"""


def parseBody(body):
    body.seek(0)
    doc = libxml2.parseDoc(body.read())
    ctxt = doc.xpathNewContext()
    ctxt.xpathRegisterNs('ac', 'http://purl.org/atom/app#')
    return (doc, ctxt)

class TestGeneric(unittest.TestCase):
    def _cleanup(self, top):
        if os.path.exists(top):
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir(top)
            
        #for f in glob.glob(os.path.join(dir, '*')):
            
        #    os.remove(f)
        #os.rmdir(dir)

    def setUp(self):
        self._cleanup(DBDIR)
        atomstore.create(DBDIR, 'bitworking.org', 'http://example.org/%s')
        self.store = atomstore.Store(DBDIR)

    def tearDown(self):
        self.store.close()


    def test_empty(self):
        index = self.store.index()
        self.assertEqual(0, len(index))

    def test_one_valid(self):
        self.store.post(BASIC_ENTRY)
        index = self.store.index()
        self.assertEqual(1, len(index))

    def test_one_min(self):
        self.store.post(MINIMUM_ENTRY)
        index = self.store.index()
        self.assertEqual(1, len(index))
        self.assertEqual(3, len(index[0]))

    def test_missing_id(self):
        try:
            self.store.post(MISSING_ID_ENTRY)
            self.assertFail("This should throw an exception.")
        except atomstore.AtomStoreExp:
            pass
        index = self.store.index()
        self.assertEqual(0, len(index))

    def test_missing_title(self):
        try:
            self.store.post(MISSING_TITLE_ENTRY)
            self.assertFail("This should throw an exception.")
        except atomstore.AtomStoreExp:
            pass
        index = self.store.index()
        self.assertEqual(0, len(index))

    def test_not_well_formed(self):
        try:
            self.store.post(NOT_WELL_FORMED_ENTRY)
            self.assertFail("This should throw an exception.")
        except atomstore.AtomStoreExp:
            pass
        index = self.store.index()
        self.assertEqual(0, len(index))

    def test_one_unicode(self):
        self.store.post(UNICODE_ENTRY)
        index = self.store.index()
        self.assertEqual(1, len(index))

    def test_two(self):
        self.store.post(BASIC_TEMPLATE % "Test \\ / \n\tTitle")
        self.store.post(BASIC_TEMPLATE % "Title2")
        index = self.store.index()
        self.assertEqual(2, len(index))
        self.assertEqual('Title2', index[0][0])
        self.assertEqual('TestTitle', index[1][0])
        d0 = libxml2.parseDoc(self.store.get(index[1][0]))
        ctxt = d0.xpathNewContext()
        ctxt.xpathRegisterNs('atom', 'http://www.w3.org/2005/Atom')
        self.assertEqual("Test \\ / \n\tTitle", ctxt.xpathEval("//atom:title")[0].get_content())
        d1 = libxml2.parseDoc(self.store.get(index[0][0]))
        ctxt = d1.xpathNewContext()
        ctxt.xpathRegisterNs('atom', 'http://www.w3.org/2005/Atom')
        self.assertEqual("Title2", ctxt.xpathEval("//atom:title")[0].get_content())

    def test_delete(self):
        self.store.post(BASIC_TEMPLATE % "Test1")
        self.store.post(BASIC_TEMPLATE % "Test2")
        self.store.post(BASIC_TEMPLATE % "Test3")
        index = self.store.index()
        self.assertEqual(3, len(index))
        self.assertEqual('Test3', index[0][0])
        self.assertEqual('Test2', index[1][0])
        self.assertEqual('Test1', index[2][0])
        self.store.delete("Test2")
        index = self.store.index()
        self.assertEqual(2, len(index))
        self.assertEqual('Test3', index[0][0])
        self.assertEqual('Test1', index[1][0])

    def test_duplicates(self):
        self.store.post(BASIC_TEMPLATE % "Test1")
        self.store.post(BASIC_TEMPLATE % "Test1")
        index = self.store.index()
        self.assertEqual(2, len(index))
        self.assertNotEqual('Test1', index[0][0])
        self.assertEqual('Test1', index[1][0])

    def test_put(self):
        self.store.post(BASIC_TEMPLATE % "Test1")
        self.store.post(BASIC_TEMPLATE % "Test2")
        index = self.store.index()
        self.assertEqual(2, len(index))
        self.assertEqual('Test2', index[0][0])
        self.assertEqual('Test1', index[1][0])
        time.sleep(1)
        self.store.put('Test1', BASIC_TEMPLATE % "Test3")
        index = self.store.index()
        self.assertEqual(2, len(index))
        self.assertEqual('Test1', index[0][0])
        self.assertEqual('Test2', index[1][0])
        d = libxml2.parseDoc(self.store.get('Test1'))
        ctxt = d.xpathNewContext()
        ctxt.xpathRegisterNs('atom', 'http://www.w3.org/2005/Atom')
        self.assertEqual("Test3", ctxt.xpathEval("//atom:title")[0].get_content())
 
    def test_delete_non_existent(self):
        self.store.delete("fred")
        index = self.store.index()
        self.assertEqual(0, len(index))

    def test_put_non_existent(self):
        try:
            self.store.put('Test1', BASIC_TEMPLATE % "Test3")
        except atomstore.AtomStoreExp:
            pass
        index = self.store.index()
        self.assertEqual(0, len(index))
        
    def test_create_with_template(self):
        config = __import__('db.config', globals(), locals(), ['local_name'])
        self.assert_(getattr(config, 'ID_TEMPLATE'))

    def test_tags(self):
        id1 = self.store.post(CATEGORY_ENTRY % ("rest", "app"))
        id2 = self.store.post(CATEGORY_ENTRY % ("fred", ""))
        id3 = self.store.post(CATEGORY_ENTRY % ("fred", "rest"))
        index = self.store.index_by('tag', 'rest')
        self.assertEqual(2, len(index))
        self.assertTrue(id1 in index)
        self.assertTrue(id3 in index)
        index = self.store.index_by('tag', 'fred')
        self.assertEqual(2, len(index))
        self.assertTrue(id2 in index)
        self.assertTrue(id3 in index)
        index = self.store.index_by('tag', 'app')
        self.assertEqual(1, len(index))
        self.assertTrue(id1 in index)

        self.store.rebuild_indices()
        index = self.store.index_by('tag', 'rest')
        self.assertEqual(2, len(index))
        self.assertTrue(id1 in index)
        self.assertTrue(id3 in index)
        index = self.store.index_by('tag', 'fred')
        self.assertEqual(2, len(index))
        self.assertTrue(id2 in index)
        self.assertTrue(id3 in index)
        index = self.store.index_by('tag', 'app')
        self.assertEqual(1, len(index))
        self.assertTrue(id1 in index)


    def test_filter(self):
        os.unlink(os.path.join(DBDIR, 'filter.py'))
        os.unlink(os.path.join(DBDIR, 'filter.pyc'))
        f = open(os.path.join(DBDIR, 'filter.py'), "w")
        f.write(only_xhtml_filter)
        f.close()
        reload(self.store.filter)
        try:
            self.store.post(MINIMUM_ENTRY)
            self.assert_("This should have failed since the content is of type text.")
        except:
            pass


    def do_test_perf(self):
        self._cleanup('dbperf')
        atomstore.create('dbperf', 'bitworking.org', 'http://bitworking.org/projects/pyapp/collection.cgi?id=%s')
        begin = time.time()
        store = atomstore.Store('dbperf')
        #print dir(store.env)
        #print dir(store.entries)
        NUM = 10000
        NTHREADS = 1
        BLOCK = NUM/NTHREADS
        threads = []
        for i in range(NTHREADS):
            threads.append(threading.Thread(target = self.thread_proc,
                                        args = (BLOCK, i*BLOCK),
                                        name = 'writer %d' % i
                                        )
                    )
        for t in threads:
            t.start()
        # Wait for all the threads to complete.
        for t in threads:
            t.join()
        end = time.time()
        print "Time to add one entry: %f ms" % (1000.0 * (end - begin)/float(NUM))
        print "Total Time to add %d entries: %f s" % (NUM, end - begin)
        begin = time.time()
        for i in range(NUM):
            store.get(str(random.randint(0, NUM-1)))
        end = time.time()
        print "Time to read one entry: %f ms" % (1000.0 * (end - begin)/float(NUM))
        print "Total Time to read %d entries: %f s" % (NUM, end - begin)
        store.close()

    def thread_proc(self, num, start_index):
        store = atomstore.Store('dbperf')
        for i in range(num):
            store.post(BASIC_TEMPLATE % str(i+start_index))

    def _get_date(self, id):
        entry = self.store.get(id)
        doc = libxml2.parseDoc(entry)
        ctxt = doc.xpathNewContext()
        ctxt.xpathRegisterNs('atom', 'http://www.w3.org/2005/Atom')
        return ctxt.xpathEval("//atom:updated")[0].get_content()


#    def test_search(self):
#        self.store.post(BASIC_TEMPLATE % "Test1")
#        self.store.post(BASIC_TEMPLATE % "Test2")
#        self.store.post(BASIC_TEMPLATE % "Test3")
#        self.assertEqual(3, len(self.store.search('test')))
#        self.assertEqual(0, len(self.store.search('barney')))
#        self.assertEqual('Test2', self.store.search('est2')[0])

if __name__ == "__main__":
    unittest.main()

