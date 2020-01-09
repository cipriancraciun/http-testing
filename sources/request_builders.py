

from crypto import *
import http # recursive-import
from transcript import *




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
		self._extends = []
		self._forking = False
		self._fingerprint = None
	
	
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
		_builder._fingerprint = None
		return _builder
	
	def with_host (self, _host) :
		_builder = self._fork_perhaps ()
		if _builder._host is not None :
			raise Exception (0x13c5e1c8)
		_builder._host = _host
		_builder._fingerprint = None
		return _builder
	
	def with_method (self, _method) :
		_builder = self._fork_perhaps ()
		if _builder._method is not None :
			raise Exception (0x7c78c34e)
		_builder._method = _method
		_builder._fingerprint = None
		return _builder
	
	def with_path (self, _path) :
		_builder = self._fork_perhaps ()
		if _builder._path is None :
			_builder._path = list ()
		_builder._path.append (_path)
		_builder._fingerprint = None
		return _builder
	
	def with_query (self, *_query_list, **_query_dict) :
		_builder = self._fork_perhaps ()
		if _builder._query is None :
			_builder._query = list ()
		if len (_query_list) > 0 :
			_builder._query.extend (_query_list)
		if len (_query_dict) > 0 :
			_builder._query.append (_query_dict)
		_builder._fingerprint = None
		return _builder
	
	def with_path_and_query (self, _path_and_query) :
		if not isinstance (_path_and_query, basestring) :
			raise Exception (0x74099c42)
		if "?" in _path_and_query :
			_path, _query = _path_and_query.split ("?", 1)
			_query = [_query for _query in _query.split ("&") if _query != ""]
			_query = [(tuple (_query.split ("=", 1)) if "=" in _query else _query) for _query in _query]
			return self.with_path (_path) .with_query (_query)
		else :
			return self.with_path (_path_and_query)
	
	def with_header (self, _name, _value) :
		return self.with_headers ((_name, _value))
	
	def with_headers (self, _headers) :
		_builder = self._fork_perhaps ()
		if _builder._headers is None :
			_builder._headers = list ()
		_builder._headers.append (_headers)
		_builder._fingerprint = None
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
	
	
	
	
	def extend (self, _builder) :
		_builder_0 = _builder._fork_perhaps ()
		_builder = self._fork_perhaps ()
		_builder._extends.append (_builder_0)
		_builder._fingerprint = None
		return _builder
	
	
	
	
	def build (self, _transaction) :
		
		_endpoint, _host, _method, _path, _query, _headers, _body = self._build_with_extends ()
		
		if len (_query) == 0 :
			_query = None
		if len (_headers) == 0 :
			_headers = None
		
		_request = http.Request (_endpoint, _host, _method, _path, _query, _headers, _body)
		
		return _request
	
	
	def _build_with_extends (self) :
		
		_endpoint, _host, _method, _path, _query, _headers, _body = self._build_without_extends ()
		
		_builder = self
		while _builder is not None :
			
			for _builder_0 in _builder._extends :
				
				_endpoint_0, _host_0, _method_0, _path_0, _query_0, _headers_0, _body_0 = _builder_0._build_with_extends ()
				
				if _endpoint_0 is not None :
					if _endpoint is None :
						_endpoint = _endpoint_0
					else :
						raise Exception (0x3ac04f81)
				
				if _host_0 is not None :
					if _host is None :
						_host = _host_0
					else :
						raise Exception (0xc30d7933)
				
				if _method_0 is not None :
					if _method is None :
						_method = _method_0
					else :
						raise Exception (0xdb3d5120)
				
				if _path_0 is not None :
					if _path is None :
						_path = _path_0
					else :
						raise Exception (0x7a12b45c)
				
				if _query_0 is not None :
					_query.extend (_query_0)
				
				if _headers_0 is not None :
					_headers.extend (_headers_0)
				
				if _body_0 is not None :
					if _body is None :
						_body = _body_0
					else :
						raise Exception (0x76068c57)
			
			_builder = _builder._parent
		
		return _endpoint, _host, _method, _path, _query, _headers, _body
	
	
	def _build_without_extends (self) :
		
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
				for _name, _value in _source.iteritems () :
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
		
		return _endpoint, _host, _method, _path, _query, _headers, _body
	
	
	def fingerprint (self) :
		
		if self._fingerprint is not None :
			return self._fingerprint
		
		_fingerprint = list ()
		
		if self._parent is not None :
			_fingerprint.append (self._parent.fingerprint ())
		else :
			_fingerprint.append (None)
		
		_fingerprint.append ("e84243417edd533cfa85d244a7771d7a")
		_fingerprint.append (self._endpoint)
		_fingerprint.append (self._host)
		_fingerprint.append (self._method)
		_fingerprint.append (self._path)
		_fingerprint.append (self._query)
		_fingerprint.append (self._headers)
		_fingerprint.append (self._body)
		
		_fingerprint.append ("0f4a2bdc825ad3a3d49dacb3e18dda87")
		for _extender in self._extends :
			_fingerprint.append (_extender.fingerprint ())
		
		self._fingerprint = fingerprint (_fingerprint)
		
		return self._fingerprint

