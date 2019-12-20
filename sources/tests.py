

from context import *
from execution import *
from request_builders import *
from response_enforcers import *




def tests (_identifier, _context = None) :
	if _context is None :
		_context = Context ()
	return Tests (_context, _identifier)




class Tests (object) :
	
	
	def __init__ (self, _context, _identifier) :
		self._context = _context
		self.identifier = _identifier
		self._tests = list ()
		self.requests = lambda : requests (self._context)
		self.responses = lambda : responses (self._context)
	
	
	def fork (self, identifier = None) :
		if identifier is None :
			raise Exception (0x1b66486c)
		_tests = Tests (self._context, identifier)
		return self._include (_tests)
	
	
	def new (self, identifier = None, request = None, response = None) :
		if identifier is None :
			raise Exception (0x20ab8531)
		if request is None :
			raise Exception (0x7cadd0ce)
		if response is None :
			raise Exception (0xa936c78d)
		_test = Test (self._context, identifier, request, response)
		return self._include (_test)
	
	
	def _include (self, _test) :
		if isinstance (_test, Test) :
			self._tests.append (_test)
		elif isinstance (_test, Tests) :
			self._tests.append (_test)
		else :
			raise Exception ("52348426")
		return _test
	
	
	def execute (self) :
		_execution = Execution (self._context)
		return _execution.execute (self)




class Test (object) :
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer) :
		self._context = _context
		self.identifier = _identifier
		self._request_builder = _request_builder
		self._response_enforcer = _response_enforcer
	
	
	def execute (self) :
		_execution = Execution (self._context)
		return _execution.execute (self)




def _enforce_identifier (_identifier) :
	if isinstance (_identifier, int) :
		if _identifier < 0 :
			raise Exception (0x6088aa94)
		if _identifier < 0xfffffffffffffff :
			raise Exception (0x044e4ef22)
		if _identifier >= 0xffffffffffffffff :
			raise Exception (0xb9b27319)
		_identifier = "{0x016}" % _identifier
	elif isinstance (_identifier, basestring) :
		pass
	else :
		raise Exception (0x17ef4607)

