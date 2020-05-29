#!/usr/bin/python

import cgitb; cgitb.enable()

if False == dispatcher.dispatch(os.environ.get('REQUEST_METHOD', 'GET')):

# Do both cases, the restful one:
# if ?id=NN is present, we are talking to the 'edit-entry' URI
# if ?id=NN is not present, then we are talking to the 'create-entry' URI

# atom.cgi is the 'edit-entry' URI
# does the create and edit

class RootDispatch(dispatch.BaseHttpDispatch):
	def __init__(self, fileID):
		self.id = str(fileID)

	def POST_xml(self):
		content = sys.stdin.read()
		newItemId = getNewFileName(self.id, content)
		newItemStream = file(os.path.join(config.data_dir, str(newItemId)), "w")
		content = fixupItemContent(str(newItemId), content)
		content = addTimeStamp(content)
		newItemStream.write(content)
		newItemStream.close()
		os.chmod(os.path.join(config.data_dir, str(newItemId)), 0664)
		rebuildStaticFiles()
		newLocation = config.base_uri + str(newItemId)
		print """Status: 201 Created
Content-type: text/html
Location: %s

<html><body><h1>New Item Created.</h1><a href="%s">%s</a></body></html>\n""" % (newLocation, newLocation, newLocation)

if __name__ == "__main__":

	if False == dispatcher.dispatch(os.environ.get('REQUEST_METHOD', 'GET')):
		dispatch.fileNotFound()		
