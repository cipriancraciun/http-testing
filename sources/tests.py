

from context import *
from execution import *
from request_builders import *
from response_enforcers import *
from transcript import *




def tests (_identifier, _context = None, requests = None, responses = None, debug = None) :
	if _context is None :
		_context = Context ()
	_tests = Tests (_context, _identifier, None, None, debug)
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
	
	
	def _perhaps_requests (self, _requests) :
		if isinstance (_requests, RequestBuilder) :
			return _requests
		elif isinstance (_requests, Chainer) :
			return _chainer_apply (_requests, self.requests.fork ())
		elif _requests is None :
			return self.requests.fork ()
		else :
			raise Exception (0x4eb43ff0)
	
	def _perhaps_responses (self, _responses) :
		if isinstance (_responses, ResponseEnforcer) :
			return _responses
		elif isinstance (_responses, Chainer) :
			return _chainer_apply (_responses, self.responses.fork ())
		elif _responses is None :
			return self.responses.fork ()
		else :
			raise Exception (0xf88b4f0d)




class Tests (TestBase) :
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug) :
		TestBase.__init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug)
		self._tests = list ()
	
	
	def fork (self, identifier = None, requests = None, responses = None, debug = None) :
		_request_builder = self._perhaps_requests (requests)
		_response_enforcer = self._perhaps_responses (responses)
		_tests = Tests (self._context, identifier, _request_builder, _response_enforcer, debug)
		return self._include (_tests)
	
	
	def new (self, identifier = None, requests = None, responses = None, debug = None) :
		_request_builder = self._perhaps_requests (requests)
		_response_enforcer = self._perhaps_responses (responses)
		_test = Test (self._context, identifier, _request_builder, _response_enforcer, debug)
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




class Chainer (object) :
	
	
	def __init__ (self, _callbacks) :
		self._callbacks = _callbacks
	
	
	def __getattribute__ (self, _name) :
		
		_chainer = self
		_callbacks = object.__getattribute__ (_chainer, "_callbacks")
		
		if _callbacks is None or _name == "new" :
			if _callbacks is not None :
				_callbacks = list (_callbacks)
			else :
				_callbacks = list ()
			_chainer = Chainer (_callbacks)
		
		def _callback (*_arguments_list, **_arguments_dict) :
			
			if _name == "new" :
				
				if len (_arguments_list) > 0 :
					raise Exception (0x0cfe9b27)
				if len (_arguments_dict) > 0 :
					raise Exception (0xdd1a0531)
				
			else :
				_callbacks.append ((_name, _arguments_list, _arguments_dict))
			
			return _chainer
		
		return _callback


chain = Chainer (None)


def _chainer_apply (_chainer, _self) :
	
	_callbacks = object.__getattribute__ (_chainer, "_callbacks")
	
	if _callbacks is not None :
		for _name, _arguments_list, _arguments_dict in _callbacks :
			_callback = getattr (_self, _name)
			_self = _callback (*_arguments_list, **_arguments_dict)
	
	return _self




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

