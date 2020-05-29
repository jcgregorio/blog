import kid
import os
import simplejson

extensions = {
    'html': 'text/html',
    #'xhtml': 'application/xhtml+xml',
    'xhtml': 'text/html; charset="utf-8"',
    'atom': 'application/atom+xml',
    'js': 'application/x-javascript'
}

def render(start_response, template_file, vars):
    ext = template_file.rsplit(".")
    contenttype = "text/html"
    if len(ext) > 1 and (ext[1] in extensions):
        contenttype = extensions[ext[1]]
    
    template = kid.Template(file=os.path.join('templates', template_file), **vars)
    body = template.serialize(output="xhtml", encoding='utf-8')
    start_response("200 OK", [('Content-Type', contenttype)])
    return [body]

def expand_uri_template(uri, params):
    # Add braces around each of the keys and %-expand all the values
    quoted_params = dict([("{%s}" % key, urllib.quote(value.encode('utf-8'))) 
        for key, value in params.iteritems()])

    # define a function that we will later use to do the
    # regular expression substitution. Replace matches
    # only if they have valus in quoted_uri_parameters.
    def replace(match):
        return quoted_params.get(match.group(0), match.group(0))

    return re.sub(r"{.*?}", replace, uri)

def render_json(start_response, struct):
    body = simplejson.dumps(struct)
    start_response("200 OK", [('Content-Type', 'text/plain')])
    return [body]


