

import http # recursive-import




def requests (_context = None) :
	if _context is None :
		_context = Context ()
	return RequestBuilder (_context, None)




class RequestBuilder (object) :
	
	
	def __init__ (self, _context, _parent) :
		self._context = _context
		self._parent = _parent
		self._endpoint = None
		self._host = None
		self._method = None
		self._path = None
		self._query = None
		self._headers = None
		self._body = None
		self._forking = False
	
	
	def fork (self) :
		return RequestBuilder (self._context, self)
	
	def forker (self) :
		_builder = self.fork ()
		_builder._forking = True
		return _builder
	
	def _fork_perhaps (self) :
		if self._forking :
			return self.fork ()
		else :
			return self
	
	
	def with_endpoint (self, _endpoint) :
		_builder = self._fork_perhaps ()
		if _builder._endpoint is not None :
			raise Exception (0xf11cb2b1)
		_builder._endpoint = _endpoint
		return _builder
	
	def with_host (self, _host) :
		_builder = self._fork_perhaps ()
		if _builder._host is not None :
			raise Exception (0x13c5e1c8)
		_builder._host = _host
		return _builder
	
	def with_method (self, _method) :
		_builder = self._fork_perhaps ()
		if _builder._method is not None :
			raise Exception (0x7c78c34e)
		_builder._method = _method
		return _builder
	
	def with_path (self, _path) :
		_builder = self._fork_perhaps ()
		if _builder._path is not None :
			_path = [_builder._path, _path]
		_builder._path = _path
		return _builder
	
	def with_query (self, **_query) :
		_builder = self._fork_perhaps ()
		if _builder._query is not None :
			_query = [_builder._query, _query]
		_builder._query = _query
		return _builder
	
	def with_headers (self, _headers) :
		_builder = self._fork_perhaps ()
		if _builder._headers is not None :
			_headers = [_builder._headers, _headers]
		_builder._headers = _headers
		return _builder
	
	
	def head (self, _path, **_query) :
		return self._generic ("HEAD", _path, _query)
	
	def get (self, _path, **_query) :
		return self._generic ("GET", _path, _query)
	
	def put (self, _path, _body, **_query) :
		return self._generic ("PUT", _path, _query)
	
	def post (self, _path, _body, **_query) :
		return self._generic ("POST", _path, _query)
	
	def patch (self, _path, _body, **_query) :
		return self._generic ("PATCH", _path, _query)
	
	def delete (self, _path, **_query) :
		return self._generic ("DELETE", _path, _query)
	
	def options (self, _path, **_query) :
		return self._generic ("OPTIONS", _path, _query)
	
	def _generic (self, _method, _path, _query) :
		_builder = self
		_builder = _builder.with_method (_method)
		_builder = _builder.with_path (_path)
		_builder = _builder.with_query (_query)
		return _builder
	
	
	def build (self, _transaction) :
		
		_endpoint = None
		_host = None
		_method = None
		_path = None
		_query = list ()
		_headers = list ()
		_body = None
		
		def _merge (_target, _source, _without_value_allowed = False) :
			if _source is None :
				pass
			elif isinstance (_source, basestring) :
				if not _without_value_allowed :
					raise Exception (0xd7127ecb)
				_target.append (_source)
			elif isinstance (_source, list) :
				for _source in _source :
					_merge (_target, _source, _without_value_allowed)
			elif isinstance (_source, tuple) :
				if len (_source) < 1 :
					raise Exception (0x769ab01b)
				_name = _source[0]
				if not isinstance (_name, basestring) :
					raise Exception (0x9142e653)
				for _value in _source[1:] :
					if not isinstance (_value, basestring) :
						raise Exception (0x0810f669)
					_target.append ((_name, _value))
			elif isinstance (_source, dict) :
				for _name, _value in _source :
					_merge (_target, (_name, _value), _without_value_allowed)
			else :
				raise Exception (0x1f49dbdc)
		
		_builder = self
		while _builder is not None :
			
			if _endpoint is None and _builder._endpoint is not None :
				_endpoint = _builder._endpoint
			
			if _host is None and _builder._host is not None :
				_host = _builder._host
			
			if _method is None and _builder._method is not None :
				_method = _builder._method
			
			if _path is None and _builder._path is not None :
				_path = _builder._path
			
			if _body is None and _builder._body is not None :
				_body = _builder._body
			
			_merge (_query, _builder._query, True)
			_merge (_headers, _builder._headers, False)
			
			_builder = _builder._parent
		
		if len (_query) == 0 :
			_query = None
		if len (_headers) == 0 :
			_headers = None
		
		_request = http.Request (_endpoint, _host, _method, _path, _query, _headers, _body)
		
		return _request

