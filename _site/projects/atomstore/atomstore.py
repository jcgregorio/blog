#!/usr/bin/python
"""
  AtomStore allows for efficient storage, retrieval
  and updating of Atom Entries. In addition there is
  a separate command line tool, ats, for manipulating
  AtomStores.
     
  Each store is a directory populated with  
  some Python code and the data.

  We store a template for the atom:id function in
  __init__.py. The 'create' function creates a default
  template which you can update after the store
  has been created.


  TODO:
  - Add an 'apply()' method that allows applying some 
    tranformation to each entry in the store.
  - Add more specific 'index' functions for getting subsets 
    of the index, for example, ones that conform to 
    PaceSimplifyCollections.
  - Add a callback that gets triggered on a POST or PUT.
    The callback can modify the entry as need be, for example,
    adding link rel="alternate" and rel="edit"
"""

from pysqlite2 import dbapi2 as sqlite
import os
import sys
import re
import random
import time
from elementtree.ElementTree import ElementTree, SubElement, XML, tostring
from cStringIO import StringIO

_DEFAULT_ID_TEMPLATE  = "tag:bitworking.org,2005:db:%s"
_DEFAULT_URI_TEMPLATE  = "%s"
ATOM = "http://www.w3.org/2005/Atom"
ATOM_TITLE = '{%s}title' % ATOM
ATOM_LINK = '{%s}link' % ATOM
ATOM_UPDATED = '{%s}updated' % ATOM
ATOM_ID = '{%s}id' % ATOM
ATOM_ENTRY = '{%s}entry' % ATOM

class AtomStoreExp(Exception):
    """All exceptions raised in this module
       are of this class
    """
    def __init__(self, args=None):
        self.args = args

def _open(dbdir):
    db_path = os.path.join(dbdir, 'entries.db')
    create_tables = False 
    if not os.path.exists(db_path):
        create_tables = True

    con = sqlite.connect(db_path, timeout=20)
    con.row_factory = sqlite.Row
    cur = con.cursor()
    if create_tables:
        cur.execute("create table store(id text primary key, title text, last_modified real, created real, entry text)")
    return (con, cur)


config_default = """
# This file is used to define basic configuration values
# for this Atom Store.

# The ID_TEMPLATE is a templated string that takes only a single %%s where the raw entry id 
# gets plaed to make a complete atom:id.
ID_TEMPLATE = 'tag:%s,%04d-%02d-%02d:%s:%%s'

# The EDIT_URI_TEMPLATE defines a parametrized string, again
# with a %%s where the raw entry id goes, that defines the edit
# URI for the entry.
EDIT_URI_TEMPLATE = '%s' """ 

index_default = """
# This file is used to define extra indices for entries.
ATOM = "http://www.w3.org/2005/Atom"
ATOM_CATEGORY = '{%s}category' % ATOM

def parse_tags(entry):
    # entry is an entry pre-parsed into an elementtree.
    terms = [e.get('term', '') for e in entry.findall(ATOM_CATEGORY)]
    return [t.lower() for t in terms if t] 

# A list of tuples, each tuple 
# is a table name, the type of the 'value' we
# are indexing on, and a function that takes
# and elementtree parsed entry and returns a list
# of values that the entry will be indexed on.
tables = [('tag', 'text', parse_tags)]

"""

filter_default = """
# This file is used to filter incoming entries.
# The single function check() takes an elementtree
# parsed entry and returns the same or modified
# elementtree, or None if the entry is invalid.

def check(tree):
    return tree
"""

def create(dbdir, dname, edit_uri_template):
    """
    Create a new atom store, in the directory 'dbdir' and with
    a domain of 'dname'. The value of dname is either a
    domain name or an email address. Both of these
    values are used in generating the atom:id for each
    entry put into the store. See the specification
    for the tag: URI scheme on the appropriate choice
    for 'dname'.


    There are three Python files in db directory

    config  - basic config info
    index   - different ways entries are indexed
    filter  - modifies and validates incoming entries (this
              can also modify entries)
 
    """
    try:
        os.mkdir(dbdir)
    except os.error:
        raise AtomStoreExp("The directory %s already exists." % dbdir) 
    try:
        _open(dbdir)
    except os.error:
        raise AtomStoreExp("Failed to create database.") 
    
    # Now create the __init__.py module in the directory
    now = time.localtime()
    default_files = {
       'index.py': index_default,
       'config.py': config_default % (dname, now[0], now[1], now[2], dbdir, edit_uri_template),
       'filter.py': filter_default,
       '__init__.py': "",
    }
    for filename, contents in default_files.iteritems():
        f = open(os.path.join(dbdir, filename), "w")
        f.write(contents)
        f.close()

    store = Store(dbdir)
    store._create_index_tables()


class Store:
    """Class for manipulating Atom Stores. 
    """
    def __init__(self, dbdir = 'db'):
        """
        dbdir - name of the directory that the Atom Entries are stored in.
        """
        self.dbdir = dbdir
        self.con, self.cur = _open(self.dbdir)
        self.ID_TEMPLATE = _DEFAULT_ID_TEMPLATE
        self.EDIT_URI_TEMPLATE = _DEFAULT_URI_TEMPLATE
        # Pick up the local <dbdir>/customization files.
        config = __import__(dbdir + ".config", globals(), locals(), ['local_name'])
        self.ID_TEMPLATE = config.ID_TEMPLATE
        self.EDIT_URI_TEMPLATE = config.EDIT_URI_TEMPLATE
        """
        Add config.author
        and a way to generate an 'atom:id' for the feed.
        """

        self.indices = __import__(dbdir + ".index", globals(), locals(), ['local_name'])
        self.filter = __import__(dbdir + ".filter", globals(), locals(), ['local_name'])
       
    def _id_exists(self, id):
        subset = [row for row in self.cur.execute("select id from store where id='%s'" % id)]
        return len(subset) > 0 
    
    def _id_from_title(self, etree):
        try:
            title = etree.findall(ATOM_TITLE)[0].text
            if not title:
                title = ""
        except:
            raise AtomStoreExp, "Not a valid Atom Entry: Missing an atom:title element."
        title = re.sub("[^a-zA-Z0-9\-]+", "", title)
        while len(title) == 0 or self._id_exists(title):
            title = title + "".join(["ABCDEFGHIJKLMONOPQRSTUVWXYZ"[random.randint(0, 25)] for i in range(5)])
        return title

    def _set_path(self, etree, path, value):
        ele_lst = etree.findall(path)
        if not ele_lst:
            raise AtomStoreExp("Not a valid Atom Entry: Missing a required element.")
        ele = ele_lst[0]
        ele.clear()
        ele.text = value
    
    def id_to_uri_id(self, id):
        return self.ID_TEMPLATE % id

    def id_to_edit_uri(self, id):
        return self.EDIT_URI_TEMPLATE % id

    def _set_atom_id(self, etree, id):
        self._set_path(etree, ATOM_ID, self.id_to_uri_id(id))

    def time_to_datestring(self, now):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))

    def _set_updated(self, etree, now):
        datestring = self.time_to_datestring(now)
        self._set_path(etree, ATOM_UPDATED, datestring)

    def _set_link_rel_edit(self, etree, id):
        reledit = [e for e in etree.findall(ATOM_LINK) if e.get('rel', '') == 'edit']
        if not reledit:
            new_lin = SubElement(etree.getroot(), ATOM_LINK)
            new_lin.set('rel', 'edit')
            new_lin.set('href', self.EDIT_URI_TEMPLATE % id)
        else:
            reledit[0].set('href', self.EDIT_URI_TEMPLATE % id)

    def _get_title(self, etree):
        titles = [e for e in etree.findall(ATOM_TITLE)]
        return titles and titles[0].text or ""

    def get(self, id):
        """Returns the Atom Entry with the given 'id'.  """
        return self.cur.execute("select entry from store where id=?", (id, )).fetchone()[0]

    def _parse(self, entry):
        try:
            etree = ElementTree(file=StringIO(entry.encode('utf-8')))
        except:
            raise AtomStoreExp("Not a well-formed Atom Entry.")
        return etree

    def _clear_old_indices(self, id):
        if self.indices:
            for name, type, fn in self.indices.tables:
                try:
                    self.cur.execute("delete * from %s where id = ?" % name, (id,))
                except:
                    pass

    def _add_indices(self, id, entry):
        if self.indices:
            for name, type, fn in self.indices.tables:
                for value in fn(entry):                
                    self.cur.execute("insert into %s(id, value) values (?, ?)" % name, (id.encode('utf-8'), value.encode('utf-8'))) 

    def _create_index_tables(self):
        if self.indices:
            for name, type, fn in self.indices.tables:
                self.cur.execute("create table %s(id text, value %s)" % (name, type))
    
    def _delete_index_tables(self):
        if self.indices:
            for name, type, fn in self.indices.tables:
                self.cur.execute("drop table if exists %s" % (name,))

    def _index_every_entry(self):
        for row in self.index():
            etree = self._parse(self.get(row[0]))
            self._add_indices(row[0], etree)

    def _store_entry(self, id, entry):
        now = time.time()
        create = False
        if not id:
            create = True

        etree = self._parse(entry)
        if not id:
            id = self._id_from_title(etree)
        self._set_atom_id(etree, id)

        self._set_updated(etree, now)
        self._set_link_rel_edit(etree, id)
        title = self._get_title(etree)

        etree = self.filter.check(etree)

        if etree:
            updated_entry = etree.getiterator(ATOM_ENTRY)[0]
            if create:
                self.cur.execute("insert into store(id, title, last_modified, created, entry) values (?, ?, ?, ?, ?)", (id, title, now, now, tostring(updated_entry, 'utf-8')))
            else:
                self.cur.execute("update store set title=?, last_modified=?, entry=? where id=?", (title, now, tostring(updated_entry, 'utf-8'), id))
    
            if not create:
                self._clear_old_indices(id)
            self._add_indices(id, etree)
            self.con.commit()
            return (unicode(id), etree)
        else:
            raise AtomStoreExp("Entry failed to meet the requirements.")

    def post(self, entry):
        """
        Adds the 'entry' to the store. The atom:id element
        is written at this time and the atom:updated
        element is updated to reflect the current time.

        The link@rel="edit" is also added at this time.
        The URI is given in self.EDIT_URI_TEMPLATE, which 
        can be specified at store creation time.
        """
        (id, doc) = self._store_entry("", entry)

        return id

    def delete(self, id):
        """
        Removed the entry with given 'id'.
        """
        self.cur.execute("delete from store where id=?", (id, ))
        self.con.commit()

    def put(self, id, entry):
        """Updated an Atom Entry for the given 'id'.
        The atom:id value is enforced and the atom:updated
        value is updated to reflect the update.
        """
        if not self._id_exists(id):
            raise AtomStoreExp("There is no Entry in this store with that id.")
        (id, doc) = self._store_entry(id, entry)

    def index(self, length = -1, offset = 0):
        """Return the index, a list of (id, title, updated) sorted 
        by their atom:updated value, of the desired length and offset."""
        return [row for row in self.cur.execute("select id, title, last_modified from store order by last_modified desc limit %d offset %d" % (length, offset))]

    def index_by(self, index, value, length = -1, offset = 0):
        """Return the index, a list of id' of the desired length and offset
        that match the given index value."""
        return [row[0] for row in self.cur.execute("select id from %s where value = ? limit %d offset %d" % (index, length, offset), (value,))]


    # Also add a function that returns the title and updated
    # values for a given id.

    def rebuild_indices(self):
        """Call this if you change <db>/index.py in any 
        functional way. This will rebuild all the index tables."""
        self._delete_index_tables()
        self._create_index_tables()
        self._index_every_entry()

    def search(self, wordlist):
        return []
        "Returns a list of id's of entries that match.`"
        
    def apply(self, f):
        """
        Apply the transformation funtion f to each of the entries in the database.
        The function f should return either a modified doc instance
        of the updated entry, or None if the entry wasn't modified.
        """
        
    def close(self):
        """Forcibly shut down the databases.
        """
        pass


