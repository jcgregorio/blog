import os, sys

def create():
    from sqlalchemy import Table
    import model
    for (name, table) in vars(model).iteritems():
        if isinstance(table, Table):
            table.create() 

def run():
    import urls
    if os.environ.get("REQUEST_METHOD", ""):
        from wsgiref.handlers import BaseCGIHandler
        f = file("log", "a")
        BaseCGIHandler(sys.stdin, sys.stdout, f, os.environ).run(urls.urls)
        f.close()
    else:
        from wsgiref.simple_server import WSGIServer, WSGIRequestHandler 
        httpd = WSGIServer(('', 8080), WSGIRequestHandler)
        httpd.set_app(urls.urls)
        print "Serving HTTP on %s port %s ..." % httpd.socket.getsockname()
        httpd.serve_forever() 

if __name__ == "__main__":
    for (name, func) in locals().copy().iteritems():
        if callable(func) and name in sys.argv[1:]:
            func()


