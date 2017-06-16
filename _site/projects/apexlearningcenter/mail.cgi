#!/bin/env python
import cgitb; cgitb.enable()
import smtplib
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import traceback
import getopt
import sys
import string
from cgi import parse_qs
import os
import logging
import sys,os,xmpp,time

logging.basicConfig(level=logging.INFO, filemode="a", format='%(asctime)s %(levelname)s %(message)s' ,filename="/home/jcgregorio/webapps/bitworking/projects/apexlearningcenter/log")

mail_fail = False
sheet_fail = False

logging.info("Start")

size = int(os.environ.get('CONTENT_LENGTH', "-1"))
body = parse_qs(sys.stdin.read(size)) 
row = dict([(key, " ".join(value)) for key, value in body.iteritems()])


errorcode = "unknown"

def send_notification(message):

    tojid='joe.gregorio@gmail.com'
    text='Apex Learning Center Registration: ' + message 

    jidparams={}
    HOME = '/home/jcgregorio/'
    if os.access(HOME +'/.xsend',os.R_OK):
        for ln in open(HOME+'/.xsend').readlines():
            if not ln[0] in ('#',';'):
                key,val=ln.strip().split('=',1)
                jidparams[key.lower()]=val
    for mandatory in ['jid','password']:
        if mandatory not in jidparams.keys():
            logging.error("Jabber: Invalid .xsend file.")
            return

    jid=xmpp.protocol.JID(jidparams['jid'])
    cl=xmpp.Client(jid.getDomain(),debug=[])

    con=cl.connect()
    if not con:
        logging.error("Jabber: Could not connent")
        return
    auth=cl.auth(jid.getNode(),jidparams['password'],resource=jid.getResource())
    if not auth:
        logging.error("Jabber: Could not log in")
        return

    id=cl.send(xmpp.protocol.Message(tojid,text))
    time.sleep(1)   # some older servers will not send the message if you disconnect immediately after sending



try:
	fromaddr = "joe@bitworking.org"
	toaddrs  = "lynne@apexlearningcenter.com"
	ccaddrs  = "jcgregorio@google.com"
	subject = "Registration"
	msg = ("From: %s\r\nTo: %s\r\nCc: %s\r\nSubject: %s\r\n\r\n"
	   % (fromaddr, toaddrs, ccaddrs, subject))

	msg += "New registration information:\r\n"
	msg += "\r\n".join(["%s: %s" % (key, value) for key, value in row.iteritems()])

	server = smtplib.SMTP('smtp.webfaction.com')
	server.login(*(file("/home/jcgregorio/local.secret", "r").read().split()))
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
	logging.error("SMTP success")
except:
	mail_fail = True 
	errorcode = "Failed"
	logging.error("SMTP failed")

try:
	curr_key = "o09348461495030281047.1779799071219367976" 
	curr_wksht_id = "od6"

	gd_client = gdata.spreadsheet.service.SpreadsheetsService()
	email, password = file("/home/jcgregorio/apexlearningcenter.pw", "r").read().split()
	gd_client.email = email
	gd_client.password = password
	gd_client.source = "Joe Gregorio - apps for your domain pages to spreadsheet gateway"
	gd_client.ProgrammaticLogin()

	#    row = {
	#    "name": "Christopher Gregorio",
	#    "address": "1002 Heathwood Dairy Rd",
	#    "dob": "4/18/94",
	#    "phone": "272-3764",
	#    "altphone": "387-9107",
	#    "parentname": "Lynne Gregorio",
	#    "parentemail": "lynne@apexlearningcenter.com",
	#    "childemail": "xdragonx@gmail.com",
	#    "school": "Apex Middle",
	#    "track": "n/a",
	#    "courses": "100, 102, 103",
	#    }

	entry = gd_client.InsertRow(row, curr_key, curr_wksht_id)
	if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
		sheet_fail = True 
		logging.error("Adding registration to spreadsheet failed.")
		logging.error(entry)
		errorcode = "LSUSSA" # Lynne screwed up spreadsheet SHARING again
except:
	sheet_fail = True 
	logging.error("Exception when adding registration to spreadsheet.")
	logging.error("".join(traceback.format_tb(sys.exc_info()[2])))
	errorcode = "LSUSA" # Lynne screwed up spreadsheet again


# Load up the price list

lookup_curr_key = "o09348461495030281047.2744393525451891033" 
lookup_curr_wksht_id = "od6"
list_feed = gd_client.GetListFeed(lookup_curr_key, lookup_curr_wksht_id)

lookup = dict(
        [(entry.custom['code'].text.upper(), entry.custom['cost'].text) for i, entry in enumerate(list_feed.entry)]
        )


lookup_curr_wksht_id = "od7"
list_feed = gd_client.GetListFeed(lookup_curr_key, lookup_curr_wksht_id)

discount_lookup = dict(
        [(entry.custom['code'].text, entry.custom['discount'].text) for i, entry in enumerate(list_feed.entry)]
        )



# Calculate the price

course_list = row['courses'].split()
bad_classes = [] 
amount = 0
for course in course_list:
    course = course.upper()
    if course not in lookup:
        bad_classes.append(course)
    else:
        amount += int(lookup[course][1:])
amount = float(amount)

discounts = []
bad_discounts = []
if 'discount' in row:
    for discount_code in row['discount'].split(): 
        discount_code = discount_code.upper()
        if discount_code in discount_lookup:
            discounts.append(float(discount_lookup[discount_code][:-1])/100.0)
        else:
            bad_discounts.append(discount_code)
    discounts.sort()
    if discounts:
        maxd = discounts[-1]
        amount = (1.0 - maxd) * amount 


if not sheet_fail:
    print "Content-type: text/html"
    print "Status: 200 Ok"
    print
    print "<h1>Registration complete</h1>"
    if discounts:
        print "<p>You're discount code gave you a %d%% discount, which has already been applied to the total below.</p>" % (maxd * 100)
    if bad_discounts:
        print "<p>The following discount codes are invalid: %s</p>" % (" ".join(bad_discounts))
    print "<p>The total bill for your classes is <b>$%0.2f</b></p>" % amount
    if bad_classes:
        print """<h2>Warning</h2><p> Some of the class codes you entered do not appear to be valid. You should
        back up and re-check your course codes.</p>"""
        print "The bad course codes are: %s" % " ".join(bad_classes)
        send_notification("Bad Classes")
    else:
        print "<p>You can either pay using the button below, or you can bring cash or a check to the school</p>"
        print """<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
        <input type="hidden" name="cmd" value="_xclick">
        <input type="hidden" name="business" value="lynne@apexlearningcenter.com">
        <input type="hidden" name="item_name" value="Apex Learning Center">
        <input type="hidden" name="item_number" value="web">
        <input type="hidden" name="amount" value="%0.2f">
        <input type="hidden" name="no_shipping" value="0">
        <input type="hidden" name="no_note" value="1">
        <input type="hidden" name="currency_code" value="USD">
        <input type="hidden" name="lc" value="US">
        <input type="hidden" name="bn" value="PP-BuyNowBF">
        <input type="image" src="https://www.paypal.com/en_US/i/btn/x-click-butcc.gif" border="0" name="submit" alt="Make payments with PayPal - it's fast, free and secure!">
        <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1">
        </form>""" % amount
        print "<p>Click here to <a href='http://www.apexlearningcenter.com/registrationcomplete'>return to the Apex Learning Center</a>.</p>"
        logging.info("Success - " + repr(locals()))
        #send_notification("Successful Registration")
else:
    #send_notification("Failed - " + errorcode)
    print "Content-type: text/html"
    print "Status: 500 Internal Error"
    print
    print "<h1>Registration Failed</h1>"
    print "<p>We're sorry but an error occured while processing your information. You can either try again or fill out the paper form at the school.</p>"
    print "<p><a href='http://www.apexlearningcenter.com/registration'>Registration</a>.</p>"
    logging.error("Error - " + repr(locals()))



logging.info("Finished")

# TODO 
# logging
# error reporting
# input validation?
# redirection
# privacy policy

