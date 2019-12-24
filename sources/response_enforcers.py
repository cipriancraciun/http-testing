

from transcript import *




def responses (_context = None) :
	if _context is None :
		_context = Context ()
	return ResponseEnforcer (_context, None)




class ResponseEnforcer (object) :
	
	
	def __init__ (self, _context, _parent) :
		self._context = _context
		self._parent = _parent
		self._enforcers = list ()
		self._extends = list ()
		self._sanitizers = list ()
		self._forking = False
	
	
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
		return _enforcer
	
	
	
	
	def append_enforcer (self, _callback, *_arguments_list, **_arguments_dict) :
		_enforcer_0 = lambda _transaction : _callback (_transaction, *_arguments_list, **_arguments_dict)
		_enforcer = self._fork_perhaps ()
		_enforcer._enforcers.append (_enforcer_0)
		return _enforcer
	
	
	def append_sanitizer (self, _callback, *_arguments_list, **_arguments_dict) :
		_sanitizer_0 = lambda _transaction : _callback (_transaction, *_arguments_list, **_arguments_dict)
		_sanitizer = self._fork_perhaps ()
		_sanitizer._sanitizers.append (_sanitizer_0)
		return _sanitizer
	
	
	
	
	def enforce (self, _transaction) :
		
		_failed = False
		
		if self._parent is not None :
			_outcome = self._parent.enforce (_transaction)
			if _outcome is not None and _outcome is not True :
				# return _outcome
				_failed = True
		
		for _enforcer in self._enforcers :
			_outcome = _enforcer (_transaction)
			if _outcome is not None and _outcome is not True :
				# return _outcome
				_failed = True
		
		for _extender in self._extends :
			_outcome = _extender.enforce (_transaction)
			if _outcome is not None and _outcome is not True :
				# return _outcome
				_failed = True
		
		return not _failed
	
	
	
	
	def sanitize (self, _transaction) :
		
		if self._parent is not None :
			self._parent.sanitize (_transaction)
		
		for _sanitizer in self._sanitizers :
			_sanitizer (_transaction)
		
		for _extender in self._extends :
			_extender.sanitize (_transaction)

