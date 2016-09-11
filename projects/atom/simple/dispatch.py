class BaseHttpDispatch:
	"""Dispatch HTTP events based on the verb and requested Mimi-Type"""
	def dispatch(self, verb, mime_type):
		"""Pass in the verb and the simplified mime-type, i.e. html or xml, 
		and the best matching function will be called, for example
		'POST' and 'xml' will first look for 'POST_xml' and then if that fails
		it will try to call 'POST'. Returns True if any match was found."""
		returnValue = False
		fun_name = verb + "_" + mime_type
		if fun_name in dir(self) and callable(getattr(self, fun_name)):
			getattr(self, fun_name)()
			returnValue = True
		elif verb in dir(self) and callable(getattr(self, verb)):
			getattr(self, verb)()
			returnValue = True
		return returnValue

