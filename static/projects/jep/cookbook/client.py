import httplib2
import simplejson
import urlparse

h = httplib2.Http(".cache")

BASE = "http://bitworking.org/projects/jep/cookbook/main.cgi/cookbook/json/"

# Get the collection
(resp, content) = h.request(BASE)
struct = simplejson.loads(content)

# Iterate over the members in the collection
# Update each member's title
for member in struct['members']:
    abs_member = urlparse.urljoin(BASE, member['href'])
    (resp, content) = h.request(abs_member)
    struct = simplejson.loads(content)
    title = struct['title'].split(" on a stick")[0]
    struct['title'] = title + " on a stick"
    (resp, content) = h.request(abs_member, method="PUT", body=simplejson.dumps(struct))

# Add a new recipe to the collection
new_member = {
    "title": "Some random recipe",
    "instructions": "First, get a ..."
}

(resp, content) = h.request(BASE, method="POST", body=simplejson.dumps(new_member))

