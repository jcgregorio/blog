"""$Id: author.py 511 2006-03-07 05:19:10Z rubys $"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision: 511 $"
__date__ = "$Date: 2006-03-07 00:19:10 -0500 (Tue, 07 Mar 2006) $"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"
__license__ = "Python"

from base import validatorBase
from validators import *

#
# author element.
#
class author(validatorBase):
  def getExpectedAttrNames(self):
    return [(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#', u'parseType')]

  def validate(self):
    if not "name" in self.children and not "atom_name" in self.children:
      self.log(MissingElement({"parent":self.name, "element":"name"}))

  def do_name(self):
    return nonhtml(), nonemail(), nonblank(), noduplicates()

  def do_email(self):
    return addr_spec(), noduplicates()

  def do_uri(self):
    return nonblank(), rfc3987(), nows(), noduplicates()

  def do_foaf_workplaceHomepage(self):
    return rdfResourceURI()

  def do_foaf_homepage(self):
    return rdfResourceURI()

  def do_foaf_weblog(self):
    return rdfResourceURI()
  
  def do_foaf_plan(self):
    return text()
  
  def do_foaf_firstName(self):
    return text()
  
  # RSS/Atom support
  do_atom_name = do_name
  do_atom_email = do_email
  do_atom_uri = do_uri
