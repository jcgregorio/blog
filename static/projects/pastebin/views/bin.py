from robaccia.defaultmodelcollection import DefaultModelCollection
from robaccia import render, form_parser
from models.bin import table

class Collection(DefaultModelCollection):

    # GET /{view}/
    def list(self, environ, start_response):
        pass

    # GET /{view}/{id}
    def retrieve(self, environ, start_response):
        pass

    # DELETE /{view}/{id}
    def delete(self, environ, start_response):
        pass

    # POST /{view}/
    def create(self, environ, start_response):
        pass

app = Collection('html', render, form_parser, table)


