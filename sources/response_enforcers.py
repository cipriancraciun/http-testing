



def responses (_context = None) :
	if _context is None :
		_context = Context ()
	return ResponseEnforcer (_context, None)




class ResponseEnforcer (object) :
	
	
	def __init__ (self, _context, _parent) :
		self._context = _context
		self._parent = _parent
		self._enforcers = list ()
	
	
	def fork (self) :
		return ResponseEnforcer (self._context, self)
	
	
	
	
	def redirect_to (self, _location, _code = (301, 302, 303, 307, 308)) :
		return self.has_status (_code) .has_header ("Location", _location)
	
	
	
	
	def expect_200 (self) :
		return self.has_status (200)
	
	def has_status (self, _code) :
		return self.append_enforcer (self._enforce_status_code, _code)
	
	def _enforce_status_code (self, _transaction, _expected) :
		_actual = _transaction.response.status_code
		if isinstance (_expected, int) :
			if _actual != _expected :
				_transaction.annotations.error (0x79b1b50d, "status code:  expected `%d`,  received `%d`!", _expected, _actual)
				return False
		elif isinstance (_expected, list) or isinstance (_expected, tuple) or isinstance (_expected, set) :
			if _actual not in _expected :
				_transaction.annotations.error (0x79c10e29, "status code:  expected not matched,  received `%d`!", _actual)
				return False
		else :
			raise Exception (0xadc2b533)
		return True
	
	
	
	
	def has_header (self, _name, _value = True) :
		return self.append_enforcer (self._enforce_header, _name, _value)
	
	def _enforce_header (self, _transaction, _name, _expected) :
		_actual = _transaction.response.headers_0.get (_name.lower ())
		if _expected is None or _expected is False :
			if _actual is not None :
				_transaction.annotations.error (0x22844c67, "header `%s`:  expected none, received `%s`!", _name, _actual)
				return False
		elif _expected is True :
			if _actual is None :
				_transaction.annotations.error (0x41ba0fd5, "header `%s`:  expected, received none!", _name)
		elif isinstance (_expected, basestring) :
			if _actual != _expected :
				_transaction.annotations.error (0xd1ae5495, "header `%s`:  expected `%s`, received `%s`!", _name, _expected, _actual)
				return False
		elif isinstance (_expected, list) or isinstance (_expected, tuple) or isinstance (_expected, set) :
			if _actual not in _expected :
				_transaction.annotations.error (0x6015606a, "header `%s`:  expected not matched, received `%s`!", _name, _actual)
				return False
		else :
			raise Exception (0x6ce1d2c3)
		return True
	
	
	
	
	def has_body (self, _expected = True) :
		return self.append_enforcer (self._enforce_body, _expected)
	
	def _enforce_body (self, _transaction, _expected) :
		_actual = _transaction.response.body
		_actual_len = len (_actual) if _actual is not None else 0
		if _expected is None or _expected is False :
			if _actual is not None :
				_transaction.annotations.error (0x9fe82649, "body:  expected none,  received `%d`!", _actual_len)
				return False
		elif _expected is True :
			if _actual is None :
				_transaction.annotations.error (0x78dada70, "body:  expected,  received none!")
				return False
		elif isinstance (_expected, basestring) :
			if _actual is None or _actual != _expected :
				_transaction.annotations.error (0x90b47ff2, "body:  expected `%s`, received `%d`!", _expected, _actual_len)
				return False
		else :
			raise Exception (0xd36ffd83)
		return True
	
	
	
	def append_enforcer (self, _callback, *_arguments_list, **_arguments_dict) :
		_enforcer = lambda _transaction : _callback (_transaction, *_arguments_list, **_arguments_dict)
		self._enforcers.append (_enforcer)
		return self
	
	
	
	
	def enforce (self, _transaction) :
		if self._parent is not None :
			_outcome = self._parent.enforce (_transaction)
			if _outcome is not None and _outcome is not True :
				return _outcome
		for _enforcer in self._enforcers :
			_outcome = _enforcer (_transaction)
			if _outcome is not None and _outcome is not True :
				return _outcome

