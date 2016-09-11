import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string


lookup_curr_key = "o09348461495030281047.2744393525451891033" 
lookup_curr_wksht_id = "od7"

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
email, password = file("/home/jcgregorio/apexlearningcenter.pw", "r").read().split()
print email, password
gd_client.email = email
gd_client.password = password
gd_client.source = "Joe Gregorio - apps for your domain pages to spreadsheet gateway"
gd_client.ProgrammaticLogin()


list_feed = gd_client.GetListFeed(lookup_curr_key, lookup_curr_wksht_id)

lookup = dict(
        [(entry.custom['code'].text, entry.custom['discount'].text) for i, entry in enumerate(list_feed.entry)]
        )

print lookup
