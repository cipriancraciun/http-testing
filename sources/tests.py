

from context import *
from execution import *
from request_builders import *
from response_enforcers import *
from transcript import *

import request_builders, response_enforcers




def tests (identifier = None, requests = None, responses = None, debug = None, skip = None, _context = None) :
	
	if _context is None :
		_context = Context ()
	
	if isinstance (requests, Chainer) :
		requests = _chainer_apply (requests, request_builders.requests (_context))
	
	if isinstance (responses, Chainer) :
		responses = _chainer_apply (responses, response_enforcers.responses (_context))
	
	_tests = Tests (_context, identifier, requests, responses, debug, skip)
	return _tests




class TestBase (object) :
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug, _skip) :
		
		self._context = _context
		self.identifier = enforce_identifier (_identifier)
		
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
		
		self._requests_0 = _request_builder
		self._responses_0 = _response_enforcer
		
		self.requests = self._requests_0.forker ()
		self.responses = self._responses_0.forker ()
		
		self._debug = _debug
		self._skip = _skip
	
	
	def execute (self, hooks = None, parallelism = None, debug = None) :
		_executor = Executor (self._context, _hooks = hooks, _parallelism = parallelism, _debug = debug)
		_execution = _executor.execute (self)
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
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug, _skip) :
		TestBase.__init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug, _skip)
		self._tests = list ()
	
	
	def fork (self, identifier = None, requests = None, responses = None, debug = None, skip = None) :
		_request_builder = self._perhaps_requests (requests)
		_response_enforcer = self._perhaps_responses (responses)
		_tests = Tests (self._context, identifier, _request_builder, _response_enforcer, debug, skip)
		return self._include (_tests)
	
	
	def new (self, identifier = None, requests = None, responses = None, debug = None, skip = None) :
		_request_builder = self._perhaps_requests (requests)
		_response_enforcer = self._perhaps_responses (responses)
		_test = Test (self._context, identifier, _request_builder, _response_enforcer, debug, skip)
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
	
	
	def __init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug, _skip) :
		TestBase.__init__ (self, _context, _identifier, _request_builder, _response_enforcer, _debug, _skip)




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

