from os import path
import cgi

data_dir = '/home/jcgregorio/web/piki.bitworking.org/'
text_dir = path.join(data_dir, 'text')
image_dir = path.join(data_dir, 'images')
editlog_name = path.join(data_dir, 'editlog')
cgi.logfile = path.join(data_dir, 'cgi_log')
logo_string = '<div class="header"><h1>EditableWebWiki</h1></div>'
changed_time_fmt = ' . . . . [%I:%M %p]'
date_fmt = '%a %d %b %Y'
datetime_fmt = '%a %d %b %Y %I:%M %p'
show_hosts = 0                          # show hostnames?
css_url = '/piki.css'         # stylesheet link, or ''
nonexist_qm = 0                         # show '?' for nonexistent?
root_uri = 'http://piki.bitworking.org/'
base_uri = root_uri + 'piki.cgi'
atom_base_uri = root_uri + 'atom.cgi'
base_feed_uri = root_uri + 'atomfeed.cgi'
WIKIWORD_RE = '^([A-Z][a-z]+){2,}$' 
WIKIWORD_RE_INLINE = '\b([A-Z][a-z]+){2,}\b' 

