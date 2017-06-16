#!/bin/env python2.4
from routes import Mapper
import routes

m = Mapper()
m.prefix = '/projects/pyapp/collection.cgi'
m.connect('introspection', '/introspection', controller='introspection' )
m.connect('coll/:collection/:id', id="", controller='collection')

#mapper.connect(':controller/introspection', action = 'Introspection')
#mapper.connect(':controller/id/:id', action = 'CollectionMember', id=None)
#mapper.create_regs(['store', 'action', 'id', 'format'])

# acceptable action(s): index, edit

print m.generate('introspection')
print m.generate(collection='livestore')
print m.generate(collection='livestore', id='This-is-a-slug')

print m.create_regs(['collection', 'introspection'])

print m.match('/projects/pyapp/collection.cgi/coll/some-slug')
print m.match('/projects/pyapp/collection.cgi/coll')
print m.match('/projects/pyapp/collection.cgi/introspection')
#print mapper.generate(action = 'index', id='1', store='somestore', format='atom')
#print mapper.generate(action = 'edit', id='fred', store='somestore', format='atom')
#print mapper.generate(action = 'view', id='fred', store='somestore')
#print mapper.generate(action = 'view', id='fred', store='somestore', format='atom')
#print mapper.generate(store='somestore', format='atom', action='introspetion')
#
#print mapper.match('/projects/pyapp/collection.cgi/somestore/html')
#
#print mapper.match('/projects/pyapp/collection.cgi/mycoll/index/0')
#print mapper.match('/projects/pyapp/collection.cgi/id')
#print mapper.match('/projects/pyapp/collection.cgi/')
#print mapper.match('/projects/pyapp/collection.cgi/livestore/index/1/atom')
#print mapper.match('/projects/pyapp/collection.cgi/livestore/index/2/html')
#print mapper.match('/projects/pyapp/collection.cgi/mycoll/index/0')
#print mapper.match('/projects/pyapp/collection.cgi/somestore/introspection/atom')
#print mapper.match('/projects/pyapp/collection.cgi/something/id/fred/atom')
#####
