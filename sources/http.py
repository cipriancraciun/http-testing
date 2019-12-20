

import httplib


from request_builders import *
from response_enforcers import *
from transcript import *




class Request (object) :
	
	
	def __init__ (self, _endpoint, _host, _method, _path, _query, _headers, _body) :
		self.host = _host
		self.method = _method
		self.path = _path
		self.query = _query
		self.headers = _headers
		self.body = _body
		self._normalize ()
		self._set_endpoint (_endpoint)
	
	
	def _normalize (self) :
		
		if self.host == "" : self.host = None
		if self.method == "" : self.method = None
		if self.path == "" : self.path = None
		if self.query == "" : self.query = None
		if self.body == "" : self.body = None
		
		if isinstance (self.headers, dict) and len (self.headers) == 0 : self.headers = None
		
		if isinstance (self.path, tuple) or isinstance (self.path, list) :
			if len (self.query) > 0 :
				self.path = "/".join (self.path)
			else :
				self.path = None
			self.path = urllib.quote (self.path, "/")
		
		if isinstance (self.query, dict) :
			if len (self.query) > 0 :
				self.query = sorted (list (self.query))
				self.query = [urllib.quote (_name, "") + "=" + urllib.quote (_value, "") for _name, _value in self.query]
			else :
				self.query = None
		if isinstance (self.query, tuple) or isinstance (self.query, list) :
			if len (self.query) > 0 :
				self.query = [urllib.quote (_argument, "=") for _argument in self.query]
				self.query = "&".join (self.query)
			else :
				self.query = None
		
		if self.method is None : self.method = "GET"
		if self.path is None : self.path = "/"
		
		if self.host is not None and not isinstance (self.host, basestring) :
			raise Exception (0x3008da80)
		if self.method is not None and not isinstance (self.method, basestring) :
			raise Exception (0x9a58b155)
		if self.path is not None and not isinstance (self.path, basestring) :
			raise Exception (0x65ea73f8)
		if self.query is not None and not isinstance (self.query, basestring) :
			raise Exception (0x5660b2e6)
		if self.headers is not None and not isinstance (self.headers, dict) :
			raise Exception (0x83006f62)
		if self.body is not None and not isinstance (self.body, basestring) :
			raise Exception (0x90eb3aae)
		
		if self.host is not None :
			self.host = self.host.lower ()
		self.method = self.method.upper ()
	
	
	def _set_endpoint (self, _endpoint) :
		if _endpoint is None :
			self.server_endpoint = None
			self.server_tls = False
		elif isinstance (_endpoint, basestring) :
			_endpoint = _endpoint.lower ()
			if _endpoint.startswith ("http:") :
				self.server_endpoint = _endpoint[5:]
				self.server_tls = False
			elif _endpoint.startswith ("https:") :
				self.server_endpoint = _endpoint[6:]
				self.server_tls = True
			else :
				raise Exception (0x9c984b5e)
			if self.server_endpoint == "" :
				self.server_endpoint = None
		else :
			raise Exception (0x3420f3b5)
		
		if self.server_endpoint is None and self.host is not None :
			self.server_endpoint = self.host
		
		if self.server_endpoint is None :
			raise Exception (0x0ffef94e)




class Response (object) :
	
	
	def __init__ (self, _status_code, _status_version, _status_message, _headers, _body) :
		self.status_code = _status_code
		self.status_version = _status_version
		self.status_message = _status_message
		self.headers = _headers
		self.body = _body
		self._normalize ()
	
	
	def _normalize (self) :
		self.headers_0 = dict ()
		if self.headers is not None :
			for _name, _value in self.headers.iteritems () :
				_name = _name.lower ()
				if isinstance (_value, basestring) :
					pass
				elif isinstance (_value, tuple) or isinstance (_value, list) :
					_value = list (_value)
				else :
					raise Exception (0xc807bdef)
				if _name not in self.headers_0 :
					self.headers_0[_name] = _value
				else :
					_values = self.headers_0[_name]
					if isinstance (_values, basestring) :
						_values = [_values]
						self.headers_0[_name] = _values
					if isinstance (_value, basestring) :
						_values.append (_value)
					else :
						_values.extend (_value)




class Session (object) :
	
	
	def __init__ (self) :
		pass




class Transaction (object) :
	
	
	def __init__ (self, _context, _session, _request_builder, _response_enforcer) :
		
		self.context = _context
		self.session = _session
		self.request = None
		self.response = None
		self.annotations = Annotations ()
		
		self._request_builder = _request_builder
		self._response_enforcer = _response_enforcer
		self._status = "created"
		
		self._transcript = transcript (self, 0x39d1e066)
	
	
	def prepare (self) :
		self._transcript.trace (0xc7e3cdda, "preparing...")
		if self._status != "created" :
			raise Exception (0x1c587c30)
		self._status = "preparing"
		
		if isinstance (self._request_builder, RequestBuilder) :
			self.request = self._request_builder.build (self)
		elif callable (self._request_builder) :
			self.request = self._request_builder (self)
		else :
			raise Exception (0x25a59e40)
		
		if not isinstance (self.request, Request) :
			raise Exception (0x52c05f72)
		
		self._status = "prepared"
		self._transcript.trace (0x40fb50f3, "prepared;")
	
	
	def enforce (self) :
		self._transcript.trace (0xd787ec43, "enforcing...")
		if self._status != "executed" :
			raise Exception (0x30fdb113)
		self._status = "enforcing"
		
		if isinstance (self._response_enforcer, ResponseEnforcer) :
			_outcome = self._response_enforcer.enforce (self)
		elif callable (self._response_enforcer) :
			_outcome = self._response_enforcer (self)
		else :
			raise Exception (0xc1986580)
		
		if _outcome is True or _outcome is None :
			self.succeeded = True
		elif _outcome is False :
			self.succeeded = False
		else :
			raise Exception (0xf883f718)
		
		self.failed = not self.succeeded
		
		self._status = "enforced"
		self._transcript.trace (0x5ea3bc9e, "enforced;")
		return self.succeeded
	
	
	def execute (self) :
		self._transcript.trace (0x1e41cf29, "executing...")
		if self._status != "prepared" :
			raise Exception (0x293086ba)
		self._status = "executing"
		_http = self._execute_connect ()
		self._execute_request (_http)
		self._execute_response (_http)
		_http.close ()
		self._status = "executed"
		self._transcript.trace (0x21a65363, "executed;")
	
	
	def _execute_connect (self) :
		
		self._transcript.debug (0x95adb4dd, "connecting to `%s` with TLS `%s`...", self.request.server_endpoint, self.request.server_tls)
		
		if self.request.server_tls :
			_http = httplib.HTTPSConnection (
					host = self.request.server_endpoint,
					strict = True,
					timeout = 6,
				)
		else :
			_http = httplib.HTTPConnection (
					host = self.request.server_endpoint,
					strict = True,
					timeout = 6,
				)
		
		_http.connect ()
		
		return _http
	
	
	def _execute_request (self, _http) :
		
		if self.request.query is None :
			_selector = self.request.path
		else :
			_selector = self.request.path + "?" + self.request.query
		
		self._transcript.debug (0x6f1063db, "sending request `%s` to `%s`...", self.request.method, _selector)
		
		_headers = list ()
		
		if self.request.host is not None :
			_headers.append (("Host", self.request.host))
		
		if self.request.headers is not None :
			for _name, _value in self.request.headers :
				if isinstance (_value, list) :
					for _value in _value :
						_headers.append ((_name, _value))
				else :
					_headers.append ((_name, _value))
		
		if self.request.host is not None :
			self._transcript.trace (0x02551cf9, "-- host: `%s`;", len (self.request.host))
		for _name, _value in _headers :
			self._transcript.trace (0x02551cf9, "-- header `%s`: `%s`;", _name, _value)
		if self.request.body is not None :
			self._transcript.trace (0x02551cf9, "-- body: `%d`;", len (self.request.body))
		
		# NOTE:  _http.request (self.request.method, _selector, self.request.body, _headers)
		
		_http.putrequest (self.request.method, _selector, True, True)
		
		for _name, _value in _headers :
			if _name.lower () == "content-length" :
				raise Exception (0xb9234238)
			_http.putheader (_name, _value)
		if self.request.body is not None :
			_http.putheader ("Content-Length", str (len (self.request.body)))
		elif self.request.method not in ["GET", "HEAD"] :
			_http.putheader ("Content-Length", "0")
		_http.endheaders ()
		
		if self.request.body is not None :
			_http.send (self.request.body)
		else :
			_http.send ("")
	
	
	def _execute_response (self, _http) :
		
		self._transcript.trace (0x9e154782, "receiving response...")
		
		_response = _http.getresponse ()
		
		_status_code = _response.status
		_status_version = _response.version
		_status_message = _response.reason
		
		if _status_version == 10 :
			_status_version = "1.0"
		elif _status_version == 11 :
			_status_version = "1.1"
		else :
			raise Exception (0xcb3ab75e)
		
		self._transcript.debug (0xa6fcadaf, "received response with status `%s`;", _status_code)
		self._transcript.trace (0xf1999901, "-- version: `%s`;", _status_version)
		self._transcript.trace (0xf1999901, "-- message: `%s`;", _status_message)
		
		_headers = dict ()
		for _name, _value in _response.getheaders () :
			self._transcript.trace (0x3ed4ed10, "-- header `%s`: `%s`;", _name, _value)
			if _name not in _headers :
				_headers[_name] = _value
			else :
				_values = _headers[_name]
				if isinstance (_values, basestring) :
					_values = [_values]
					_headers[_name] = _values
				_values.append (_value)
		
		_body = _response.read ()
		if len (_body) == 0 :
			_body = None
		
		if _body is not None :
			self._transcript.trace (0xffe8cfb6, "-- body: `%d`;", len (_body))
		
		self.response = Response (_status_code, _status_version, _status_message, _headers, _body)

