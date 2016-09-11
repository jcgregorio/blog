import httplib2
httplib2.debuglevel = 5
h = httplib2.Http()
h.add_credentials("joe.gregorio", "jcg@q4q4")
print h.request("https://www.google.com/history/lookup?month=1&day=3&yr=2007&output=rss")
