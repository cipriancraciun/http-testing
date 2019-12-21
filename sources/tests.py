

from context import *
from execution import *
from request_builders import *
from response_enforcers import *
from transcript import *




def tests (_identifier, _context = None, _debug = None) :
	if _context is None :
		_context = Context ()
	_tests = Tests (_context, _identifier, None, None, _debug)
	return _tests




class TestBase (object) :
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug) :
		
		if _identifier is None :
			raise Exception (0x1b66486c)
		
		self._context = _context
		self.identifier = _identifier
		
		if _request_builder is None :
			_request_builder = requests (self._context)
		elif isinstance (_request_builder, RequestBuilder) :
			pass
		else :
			raise Exception (0x6b349655)
		
		if _response_enforcer is None :
			_response_enforcer = responses (self._context)
		elif isinstance (_response_enforcer, ResponseEnforcer) :
			pass
		else :
			raise Exception (0x19f0bb59)
		
		self.requests_shared = _request_builder
		self.responses_shared = _response_enforcer
		
		self.requests = self.requests_shared.forker ()
		self.responses = self.responses_shared.forker ()
		
		self._debug = _debug
	
	
	def execute (self) :
		_execution = Execution (self._context)
		_execution.execute (self)
		return _execution




class Tests (TestBase) :
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug) :
		TestBase.__init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug)
		self._tests = list ()
	
	
	def fork (self, identifier = None, _debug = None) :
		_tests = Tests (self._context, identifier, self.requests_shared.fork (), self.responses_shared.fork (), _debug)
		return self._include (_tests)
	
	
	def new (self, identifier = None, request = None, response = None, _debug = None) :
		if identifier is None :
			raise Exception (0x20ab8531)
		_test = Test (self._context, identifier, request, response, _debug)
		return self._include (_test)
	
	
	def _include (self, _test) :
		if isinstance (_test, Test) :
			self._tests.append (_test)
		elif isinstance (_test, Tests) :
			self._tests.append (_test)
		else :
			raise Exception ("52348426")
		return _test




class Test (TestBase) :
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug) :
		TestBase.__init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug)




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

