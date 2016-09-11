import robaccia
import simplejson
from sqlalchemy import desc 
from model import recipe as table
from wsgicollection import Collection
 
primary_key = table.primary_key.columns[0]

def _load_json(environ):
    entity = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    struct = simplejson.loads(entity)
    return dict([(k.encode('us-ascii'), v) for k,v in struct.iteritems()])


class JSONCollection(Collection):

    # GET /cookbook/json/ 
    def list(self, environ, start_response):
        result = table.select().execute()    #1 
        struct = {
            "members":[{'href': "%d" % row.id} for row in result.fetchall()],
            "next": None}
        return robaccia.render_json(start_response, struct) #2

    # POST /cookbook/json/ 
    def create(self, environ, start_response):
        struct = _load_json(environ)        #3
        table.insert().execute(**struct)    #4

        start_response("201 Created", [])   #5
        return []

    # GET /cookbook/json/{id}
    def retrieve(self, environ, start_response):
        id = environ['selector.vars']['id']
        result = table.select(primary_key==id).execute() 
        struct = dict(zip(result.keys, result.fetchone())) #6
        return robaccia.render_json(start_response, struct)

    # PUT /cookbook/json/{id}
    def update(self, environ, start_response):
        struct = _load_json(environ)
        id = environ['selector.vars']['id']
        table.update(primary_key==id).execute(struct) #7 

        start_response("200 OK", [])
        return []

    # DELETE /cookbook/json/{id}
    def delete(self, environ, start_response):
        id = environ['selector.vars']['id']
        table.delete(primary_key==id).execute()
    
        start_response("200 OK", [])
        return []



def list(environ, start_response):
    rows = [row.title or " " for row in table.select(limit=5).execute()]
    if len(rows) < 5:
        rows.extend(["_"] * (5 - len(rows)))
    return robaccia.render(start_response, 'list.xhtml', locals())



