

import httplib
import urllib


from request_builders import *
from response_enforcers import *
from tools import *
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
		self._normalize_host ()
		self._normalize_method ()
		self._normalize_path ()
		self._normalize_query ()
		self._normalize_headers ()
		self._normalize_body ()
	
	def _normalize_host (self) :
		self.host = normalize_string_lower (self.host)
	
	def _normalize_method (self) :
		self.method = normalize_string_upper (self.method)
		if self.method is None :
			self.method = "GET"
	
	def _normalize_path (self) :
		if isinstance (self.path, basestring) :
			if self.path != "" :
				self.path = urllib.quote (self.path, "/")
			else :
				self.path = "/"
		else :
			self.path = flatten_list_or_similar (self.path, normalize_string)
			if len (self.path) > 0 :
				self.path = "/" + "/".join (self.path)
				while True :
					_path_len = len (self.path)
					self.path = self.path.replace ("//", "/")
					if _path_len == len (self.path) :
						break
				self.path = urllib.quote (self.path, "/")
			else :
				self.path = "/"
	
	def _normalize_query (self) :
		if isinstance (self.query, basestring) :
			if self.query != "" :
				self.query = urllib.quote (self.query, "&=")
			else :
				self.query = None
		else :
			self.query = flatten_multi_map (self.query, normalize_string, None, normalize_string, None)
			if len (self.query) > 0 :
				self.query = sorted (list (self.query))
				self.query = ["%s=%s" % (urllib.quote (_name, ""), urllib.quote (_value, "")) for _name, _value in self.query]
				self.query = "&".join (self.query)
			else :
				self.query = None
	
	def _normalize_headers (self) :
		self.headers = flatten_multi_map (self.headers, normalize_string, None, normalize_string, None)
		if len (self.headers) == 0 :
			self.headers = None
	
	def _normalize_body (self) :
		self.body = normalize_string (self.body)
	
	
	def _set_endpoint (self, _endpoint) :
		
		_endpoint = normalize_string_lower (_endpoint)
		if _endpoint is not None :
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
			self.server_endpoint = None
			self.server_tls = False
		
		if self.server_endpoint is None and self.host is not None :
			self.server_endpoint = self.host
		
		if self.server_endpoint is None :
			raise Exception (0x0ffef94e)
	
	
	def _trace (self, _tracer) :
		
		if self.host is not None :
			_tracer (0x7fc84f53, "-- host: `%s`;", self.host)
		else :
			_tracer (0xdc8cf7d9, "-- host: none;")
		
		if self.method is not None :
			_tracer (0x2ec04778, "-- method: `%s`;", self.method)
		else :
			_tracer (0xf8d40215, "-- method: unknown;")
		
		if self.path is not None :
			_tracer (0xaa0d0b82, "-- path: `%s`;", self.path)
		else :
			_tracer (0x402dd426, "-- path: unknown;")
		
		if self.query is not None :
			_tracer (0xb4970e93, "-- query: `%s`;", self.query)
		else :
			_tracer (0x763804da, "-- query: none;")
		
		if self.headers is not None and len (self.headers) > 0 :
			for _key, _value in self.headers :
				_tracer (0xe75a9e5b, "-- header `%s`: `%s`;", _key, _value)
		else :
			_tracer (0x4ed6a4ee, "-- headers: none;")
		
		if self.body is not None :
			_tracer (0xbb5141bf, "-- body: `%d` bytes;", len (self.body))
		else :
			_tracer (0xa41d4441, "-- body: none;")




class Response (object) :
	
	
	def __init__ (self, _status_code, _status_version, _status_message, _headers, _body) :
		self.status_code = _status_code
		self.status_version = _status_version
		self.status_message = _status_message
		self.headers = _headers
		self.body = _body
		self._normalize ()
	
	
	def _normalize (self) :
		
		self.status_code = normalize_positive_integer (self.status_code)
		self.status_version = normalize_string (self.status_version)
		self.status_message = normalize_string (self.status_message)
		
		self.headers = flatten_multi_map (self.headers, normalize_string, None, normalize_string, None)
		if len (self.headers) == 0 :
			self.headers = None
		self.headers_0 = multi_map_to_dict (self.headers, normalize_string_lower, None, None, None)
		
		self.body = normalize_string (self.body)
	
	
	def _trace (self, _tracer) :
		
		if self.status_code is not None :
			_tracer (0xeaa6ad21, "-- status code: `%d`;", self.status_code)
		else :
			_tracer (0x251e03c2, "-- status code: unknown;")
		
		if self.status_version is not None :
			_tracer (0x87ca843d, "-- status version: `%s`;", self.status_version)
		else :
			_tracer (0xf2563c0a, "-- status version: unknown;")
		
		if self.status_message is not None :
			_tracer (0x8820e5f1, "-- status message: `%s`;", self.status_message)
		else :
			_tracer (0xd3428693, "-- status message: unknown;")
		
		if self.headers is not None and len (self.headers) > 0 :
			for _key, _value in self.headers :
				_tracer (0x78ba5bbe, "-- header `%s`: `%s`;", _key, _value)
		else :
			_tracer (0x0e792726, "-- headers: none;")
		
		if self.body is not None :
			_tracer (0xfea4219c, "-- body: `%d` bytes;", len (self.body))
		else :
			_tracer (0xe800f587, "-- body: none;")




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
			_headers.extend (self.request.headers)
		
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
		
		_headers = list ()
		for _name, _value in _response.getheaders () :
			self._transcript.trace (0x3ed4ed10, "-- header `%s`: `%s`;", _name, _value)
			_headers.append ((_name, _value))
		
		_body = _response.read ()
		if len (_body) == 0 :
			_body = None
		
		if _body is not None :
			self._transcript.trace (0xffe8cfb6, "-- body: `%d`;", len (_body))
		
		self.response = Response (_status_code, _status_version, _status_message, _headers, _body)
	
	
	def _trace (self, _tracer) :
		
		if self.request is not None :
			_tracer (0xa21095ed, "* request:")
			self.request._trace (_tracer)
		else :
			_tracer (0xbce1112c, "* request: none;")
		
		if self.response is not None :
			_tracer (0x80d7ba56, "* response:")
			self.response._trace (_tracer)
		else :
			_tracer (0x1c59088d, "* response: none;")
		
		if len (self.annotations._records) > 0 :
			_tracer (0x08574ba6, "* annotations:")
			for _record in self.annotations._records :
				_tracer (0xcb6c9a7b, "-- " + _record.msg, *_record.args)
		else :
			_tracer (0x0c31f78c, "* annotations: none;")

