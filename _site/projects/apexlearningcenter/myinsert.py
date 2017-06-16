import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string


curr_key = "o09348461495030281047.1779799071219367976" 
curr_wksht_id = "od6"

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
email, password = file("/home/jcgregorio/apexlearningcenter.pw", "r").read().split()
print email, password
gd_client.email = email
gd_client.password = password
gd_client.source = "Joe Gregorio - apps for your domain pages to spreadsheet gateway"
gd_client.ProgrammaticLogin()

row = {
"name": "Christopher Gregorio",
"address": "1002 Heathwood Dairy Rd",
"dob": "4/18/94",
"phone": "272-3764",
"altphone": "387-9107",
"parentname": "Lynne Gregorio",
"parentemail": "lynne@apexlearningcenter.com",
"childemail": "xdragonx@gmail.com",
"school": "Apex Middle",
"track": "n/a",
"courses": "100, 102, 103",
}

entry = gd_client.InsertRow(row, curr_key, curr_wksht_id)
if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
    print 'Inserted!'
 
