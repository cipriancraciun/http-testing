

import types

from .crypto import *
from .transcript import *




def responses (_context = None) :
	if _context is None :
		_context = Context ()
	return ResponseEnforcer (_context, None)




class ResponseEnforcer (object) :
	
	
	def __init__ (self, _context, _parent) :
		self._context = _context
		self._parent = _parent
		self._allowed_headers = None
		self._enforcers = list ()
		self._extends = list ()
		self._sanitizers = list ()
		self._forking = False
		self._fingerprint = None
	
	
	def fork (self) :
		return ResponseEnforcer (self._context, self)
	
	def forker (self) :
		_enforcer = self.fork ()
		_enforcer._forking = True
		return _enforcer
	
	def _fork_perhaps (self) :
		if self._forking :
			return self.fork ()
		else :
			return self
	
	
	
	
	def allow_header (self, _name) :
		return self.allow_headers (_name)
	
	def allow_headers (self, _headers) :
		_enforcer = self._fork_perhaps ()
		if _enforcer._allowed_headers is None :
			_enforcer._allowed_headers = set ()
		_enforcer_headers = _enforcer._allowed_headers
		def _allow (_headers) :
			if isinstance (_headers, basestring) :
				_enforcer_headers.add (_headers.lower ())
			elif isinstance (_headers, list) or isinstance (_headers, tuple) or isinstance (_headers, set) :
				for _headers in _headers :
					_allow (_headers)
			else :
				raise Exception (0xd66f16f5)
		_allow (_headers)
		_enforcer._fingerprint = None
		return _enforcer
	
	def _enforce_allowed_headers (self, _transaction) :
		_headers = set (_transaction.response.headers_0.iterkeys ())
		_should_enforce = self._enforce_allowed_headers_0 (_headers)
		if _should_enforce :
			if len (_headers) > 0 :
				for _header in sorted (_headers) :
					_transaction.annotations.warning (0x83b54dfe, "header `%s`:  not expected!", _header)
				return False
			else :
				return True
		else :
			return True
	
	def _enforce_allowed_headers_0 (self, _remaining_headers) :
		_should_enforce = False
		if self._parent is not None :
			_should_enforce |= self._parent._enforce_allowed_headers_0 (_remaining_headers)
		if self._allowed_headers is not None :
			_remaining_headers.difference_update (self._allowed_headers)
			_should_enforce |= True
		for _extender in self._extends :
			_should_enforce |= _extender._enforce_allowed_headers_0 (_remaining_headers)
		return _should_enforce
	
	
	
	
	def redirect_to (self, _location, _code = (301, 302, 303, 307, 308)) :
		return self.has_status (_code) .has_header ("Location", _location)
	
	
	
	
	def expect_200 (self) :
		return self.has_status (200)
	
	def expect_403 (self) :
		return self.has_status (403)
	
	def expect_502 (self) :
		return self.has_status (502)
	
	def has_status (self, _code) :
		_enforcer = self._fork_perhaps ()
		return _enforcer.append_enforcer (_enforcer._enforce_status_code, _code)
	
	def _enforce_status_code (self, _transaction, _expected) :
		_actual = _transaction.response.status_code
		if isinstance (_expected, int) :
			if _actual != _expected :
				_transaction.annotations.warning (0x79b1b50d, "status code:  expected `%d`,  received `%d`!", _expected, _actual)
				return False
			else :
				_transaction.annotations.debug (0xbb548cd6, "status code:  matched expected, `%d`;", _actual)
		elif isinstance (_expected, list) or isinstance (_expected, tuple) or isinstance (_expected, set) :
			if _actual not in _expected :
				_transaction.annotations.warning (0x79c10e29, "status code:  expected not in set,  received `%d`!", _actual)
				return False
			else :
				_transaction.annotations.debug (0x09058571, "status code:  matched in set, `%d`;", _actual)
		else :
			raise Exception (0xadc2b533)
		return True
	
	
	
	
	def has_header (self, _name, _value = True, _lower = False) :
		_enforcer = self._fork_perhaps ()
		return _enforcer.append_enforcer (_enforcer._enforce_header, _name, _value, _lower)
	
	def _enforce_header (self, _transaction, _name, _expected, _lower) :
		_actual = _transaction.response.headers_0.get (_name.lower ())
		if _actual is not None and _lower :
			_actual = _actual.lower ()
		if _expected is None or _expected is False :
			if _actual is not None :
				_transaction.annotations.warning (0x22844c67, "header `%s`:  expected missing, received `%s`!", _name, _actual)
				return False
			else :
				_transaction.annotations.debug (0x1339e80d, "header `%s`:  matched missing;", _name)
		elif _expected is True :
			if _actual is None :
				_transaction.annotations.warning (0x41ba0fd5, "header `%s`:  expected present, received none!", _name)
				return False
			else :
				_transaction.annotations.debug (0xcb6a7efc, "header `%s`:  matched present, `%s`;", _name, _actual)
		elif isinstance (_expected, basestring) :
			if _actual is None :
				_transaction.annotations.warning (0x6a5c7a4f, "header `%s`:  expected `%s`, received none!", _name, _expected)
				return False
			elif _actual != _expected :
				_transaction.annotations.warning (0xd1ae5495, "header `%s`:  expected `%s`, received `%s`!", _name, _expected, _actual)
				return False
			else :
				_transaction.annotations.debug (0x47061c22, "header `%s`:  matched expected, `%s`;", _name, _actual)
		elif isinstance (_expected, list) or isinstance (_expected, tuple) or isinstance (_expected, set) :
			if _actual is None :
				_transaction.annotations.warning (0x1d0875b2, "header `%s`:  expected not in set, received none!", _name)
				return False
			elif _actual not in _expected :
				_transaction.annotations.warning (0x6015606a, "header `%s`:  expected not in set, received `%s`!", _name, _actual)
				return False
			else :
				_transaction.annotations.debug (0xbcb21053, "header `%s`:  matched in set, `%s`;", _name, _actual)
		else :
			raise Exception (0x6ce1d2c3)
		return True
	
	
	
	
	def has_body (self, _expected = True) :
		_enforcer = self._fork_perhaps ()
		return _enforcer.append_enforcer (_enforcer._enforce_body, _expected)
	
	def _enforce_body (self, _transaction, _expected) :
		_actual = _transaction.response.body
		_actual_len = len (_actual) if _actual is not None else 0
		if _expected is None or _expected is False :
			if _actual is not None :
				_transaction.annotations.warning (0x9fe82649, "body:  expected missing, received `%d`!", _actual_len)
				return False
			else :
				_transaction.annotations.debug (0x319fd01f, "body:  matched missing;")
		elif _expected is True :
			if _actual is None :
				_transaction.annotations.warning (0x78dada70, "body:  expected present, received none!")
				return False
			else :
				_transaction.annotations.debug (0x997fdd5b, "body:  matched present, `%d` bytes;", _actual_len)
		elif isinstance (_expected, basestring) :
			if _actual is None or _actual != _expected :
				_transaction.annotations.warning (0x90b47ff2, "body:  expected `%s`, received `%d` bytes!", _expected, _actual_len)
				return False
			else :
				_transaction.annotations.debug (0x79917b5a, "body:  matched expected, `%d` bytes;", _actual_len)
		else :
			raise Exception (0xd36ffd83)
		return True
	
	
	
	
	def sanitize_header (self, _name, _replacement = None) :
		_enforcer = self._fork_perhaps ()
		return _enforcer.append_sanitizer (_enforcer._sanitize_header, _name, _replacement)
	
	def _sanitize_header (self, _transaction, _name, _replacement) :
		_name = _name.lower ()
		if _replacement is None :
			_replacement = "{...}"
		_actual = _transaction.response.headers_0.get (_name)
		if _actual is not None :
			_transaction.response.headers_0[_name] = _replacement
			for _index in xrange (len (_transaction.response.headers)) :
				if _transaction.response.headers[_index][0].lower () == _name :
					_transaction.response.headers[_index] = (_name, _replacement)
	
	
	
	
	def extend (self, _enforcer) :
		_enforcer_0 = _enforcer._fork_perhaps ()
		_enforcer = self._fork_perhaps ()
		_enforcer._extends.append (_enforcer_0)
		_enforcer._fingerprint = None
		return _enforcer
	
	
	
	
	def append_enforcer (self, _callback, *_arguments_list, **_arguments_dict) :
		_enforcer = self._fork_perhaps ()
		_enforcer._enforcers.append ((_callback, _arguments_list, _arguments_dict))
		_enforcer._fingerprint = None
		return _enforcer
	
	
	def append_sanitizer (self, _callback, *_arguments_list, **_arguments_dict) :
		_sanitizer = self._fork_perhaps ()
		_sanitizer._sanitizers.append ((_callback, _arguments_list, _arguments_dict))
		_sanitizer._fingerprint = None
		return _sanitizer
	
	
	
	
	def enforce (self, _transaction) :
		return self._enforce_0 (_transaction, True)
	
	def _enforce_0 (self, _transaction, _top_level) :
		
		_failed = False
		
		if self._parent is not None :
			_outcome = self._parent._enforce_0 (_transaction, False)
			if _outcome is not None and _outcome is not True :
				# return _outcome
				_failed = True
		
		for _callback, _arguments_list, _arguments_dict in self._enforcers :
			_outcome = _callback (_transaction, *_arguments_list, **_arguments_dict)
			if _outcome is not None and _outcome is not True :
				# return _outcome
				_failed = True
		
		for _extender in self._extends :
			_outcome = _extender._enforce_0 (_transaction, False)
			if _outcome is not None and _outcome is not True :
				# return _outcome
				_failed = True
		
		if _top_level :
			_outcome = self._enforce_allowed_headers (_transaction)
			if _outcome is not None and _outcome is not True :
				# return _outcome
				_failed = True
		
		return not _failed
	
	
	
	
	def sanitize (self, _transaction) :
		
		self._sanitize_0 (_transaction)
		_transaction.response._set_fingerprint ()
	
	
	def _sanitize_0 (self, _transaction) :
		
		if self._parent is not None :
			self._parent.sanitize (_transaction)
		
		for _callback, _arguments_list, _arguments_dict in self._sanitizers :
			_callback (_transaction, *_arguments_list, **_arguments_dict)
		
		for _extender in self._extends :
			_extender._sanitize_0 (_transaction)
	
	
	
	
	def fingerprint (self) :
		
		if self._fingerprint is not None :
			return self._fingerprint
		
		_fingerprint = list ()
		
		if self._parent is not None :
			_fingerprint.append (self._parent.fingerprint ())
		else :
			_fingerprint.append (None)
		
		_fingerprint.append ("51a0be3ef12d33c07eaa85cb1284a397")
		_fingerprint.append (self._allowed_headers)
		
		_fingerprint.append ("d5cc4339aaf0d7967bc5e3a8ed946dea")
		for _callback, _arguments_list, _arguments_dict in self._enforcers :
			if isinstance (_callback, types.MethodType) :
				if _callback.im_class is ResponseEnforcer :
					pass
				else :
					raise Exception (0xccce4078)
			else :
				raise Exception (0xfc8ecef2)
			_fingerprint.append ((_callback.__name__, _arguments_list, _arguments_dict))
		
		_fingerprint.append ("81d3e06596994ebb64198741bfe335c3")
		for _callback, _arguments_list, _arguments_dict in self._sanitizers :
			if isinstance (_callback, types.MethodType) :
				if _callback.im_class is ResponseEnforcer :
					pass
				else :
					raise Exception (0x2cb84554)
			else :
				raise Exception (0xc3b02aa9)
			_fingerprint.append ((_callback.__name__, _arguments_list, _arguments_dict))
		
		_fingerprint.append ("d23e5e3ca25c07d1fd1ef72f849e4e54")
		for _extender in self._extends :
			_fingerprint.append (_extender.fingerprint ())
		
		self._fingerprint = fingerprint (_fingerprint)
		
		return self._fingerprint

