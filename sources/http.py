

import httplib
import ssl
import urllib
import threading
import time


from crypto import *
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
		self._set_url ()
		self._set_fingerprint ()
	
	
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
		else :
			self.headers.sort ()
	
	def _normalize_body (self) :
		self.body = normalize_string (self.body)
		self.body_size = len (self.body) if self.body is not None else 0
		self.body_md5 = hash_md5 (self.body)
	
	
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
			self.server_tls = None
		
		if self.server_endpoint is None and self.host is not None :
			self.server_endpoint = self.host
		
		if self.server_endpoint is None :
			raise Exception (0x0ffef94e)
	
	
	def _set_url (self) :
		
		_parts = []
		
		if self.host is not None or self.server_endpoint is not None :
			
			if self.server_tls is True :
				_parts.append ("https://")
			elif self.server_tls is False :
				_parts.append ("http://")
			elif self.server_tls is None :
				_parts.append ("//")
			else :
				raise Exception (0x4440ebb2)
		
		if self.host is not None :
			_parts.append (self.host)
			
		elif self.server_endpoint is not None :
			_parts.append (self.server_endpoint)
		
		if self.path is not None :
			_parts.append (self.path)
		else :
			raise Exception (0x761a7c95)
		
		if self.query is not None :
			_parts.append ("?")
			_parts.append (self.query)
		
		self.url = "".join (_parts)
		self.url_fingerprint = hash_md5 (self.url)
	
	
	def _set_fingerprint (self) :
		self.fingerprint = fingerprint ((
				"f40903d40bee0f61efb02251b875fa6f",
				self.server_endpoint,
				self.server_tls,
				self.host,
				self.method,
				self.path,
				self.query,
				self.headers,
				self.body_md5,
			))
	
	
	def _trace (self, _tracer) :
		
		_tracer (0x2a907274, "url: `%s`;", self.url)
		_tracer (0x491ef60a, "url fingerprint: `%s`;", self.url_fingerprint)
		
		if self.host is not None :
			_tracer (0x7fc84f53, "host: `%s`;", self.host)
		else :
			_tracer (0xdc8cf7d9, "host: none;")
		
		if self.method is not None :
			_tracer (0x2ec04778, "method: `%s`;", self.method)
		else :
			_tracer (0xf8d40215, "method: unknown;")
		
		if self.path is not None :
			_tracer (0xaa0d0b82, "path: `%s`;", self.path)
		else :
			_tracer (0x402dd426, "path: unknown;")
		
		if self.query is not None :
			_tracer (0xb4970e93, "query: `%s`;", self.query)
		else :
			_tracer (0x763804da, "query: none;")
		
		if self.headers is not None and len (self.headers) > 0 :
			for _key, _value in self.headers :
				_tracer (0xe75a9e5b, "header `%s`: `%s`;", _key, _value)
		else :
			_tracer (0x4ed6a4ee, "headers: none;")
		
		if self.body is not None :
			_tracer (0xbb5141bf, "body: `%d` bytes;  md5: `%s`;", self.body_size, self.body_md5)
		else :
			_tracer (0xa41d4441, "body: none;")
		
		if self.server_endpoint is not None :
			_tracer (0xbb66c295, "server endpoint: `%s`;  tls: `%s`;", self.server_endpoint, self.server_tls)
		
		if self.fingerprint is not None :
			_tracer (0x2fa37fce, "fingerprint: `%s`;", self.fingerprint)




class Response (object) :
	
	
	def __init__ (self, _status_code, _status_version, _status_message, _headers, _body) :
		self.status_code = _status_code
		self.status_version = _status_version
		self.status_message = _status_message
		self.headers = _headers
		self.body = _body
		self._normalize ()
		self._set_fingerprint ()
	
	
	def _normalize (self) :
		
		self.status_code = normalize_positive_integer (self.status_code)
		self.status_version = normalize_string (self.status_version)
		self.status_message = normalize_string (self.status_message)
		
		self.headers = flatten_multi_map (self.headers, normalize_string, None, normalize_string, None)
		if len (self.headers) == 0 :
			self.headers = None
		else :
			self.headers.sort ()
		
		self.headers_0 = multi_map_to_dict (self.headers, normalize_string_lower, None, None, None)
		
		self.body = normalize_string (self.body)
		self.body_size = len (self.body) if self.body is not None else 0
		self.body_md5 = hash_md5 (self.body)
	
	
	def _set_fingerprint (self) :
		self.fingerprint = fingerprint ((
				"314247a38774af77e4ac369f1ccface1",
				self.status_code,
				self.status_message,
				self.headers,
				self.body,
			))
	
	def _trace (self, _tracer) :
		
		if self.status_code is not None :
			_tracer (0xeaa6ad21, "status code: `%d`;", self.status_code)
		else :
			_tracer (0x251e03c2, "status code: unknown;")
		
		if self.status_version is not None :
			_tracer (0x87ca843d, "status version: `%s`;", self.status_version)
		else :
			_tracer (0xf2563c0a, "status version: unknown;")
		
		if self.status_message is not None :
			_tracer (0x8820e5f1, "status message: `%s`;", self.status_message)
		else :
			_tracer (0xd3428693, "status message: unknown;")
		
		if self.headers is not None and len (self.headers) > 0 :
			for _key, _value in self.headers :
				_tracer (0x78ba5bbe, "header `%s`: `%s`;", _key, _value)
		else :
			_tracer (0x0e792726, "headers: none;")
		
		if self.body is not None :
			_tracer (0xfea4219c, "body: `%d` bytes;  md5: `%s`;", self.body_size, self.body_md5)
		else :
			_tracer (0xe800f587, "body: none;")
		
		if self.fingerprint is not None :
			_tracer (0x7bf3732b, "fingerprint: `%s`;", self.fingerprint)




class Session (object) :
	
	
	def __init__ (self) :
		pass




class Transaction (object) :
	
	
	def __init__ (self, _context, _transport, _session, _request_builder, _response_enforcer) :
		
		self.context = _context
		self.transport = _transport
		self.session = _session
		self.request = None
		self.response = None
		self.annotations = Annotations ()
		
		self._request_builder = _request_builder
		self._response_enforcer = _response_enforcer
		self._status = "created"
		
		self._transcript = transcript (self, 0x39d1e066)
	
	
	def prepare (self) :
		self._transcript.internal (0xc7e3cdda, "preparing...")
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
		self._transcript.internal (0x40fb50f3, "prepared;")
	
	
	def enforce (self) :
		self._transcript.internal (0xd787ec43, "enforcing...")
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
		self._transcript.internal (0x5ea3bc9e, "enforced;")
		return self.succeeded
	
	
	def sanitize (self) :
		self._transcript.internal (0xd787ec43, "sanitizing...")
		if self._status != "enforced" :
			raise Exception (0x5af3ef21)
		self._status = "sanitizing"
		
		if isinstance (self._response_enforcer, ResponseEnforcer) :
			self._response_enforcer.sanitize (self)
		elif callable (self._response_enforcer) :
			pass
		else :
			raise Exception (0x520a335c)
		
		self._status = "sanitized"
		self._transcript.internal (0xa4739ad4, "sanitized;")
	
	
	def execute (self) :
		self._transcript.internal (0x1e41cf29, "executing...")
		if self._status != "prepared" :
			raise Exception (0x293086ba)
		self._status = "executing"
		_connection = self._execute_connect ()
		self._execute_request (_connection)
		self._execute_response (_connection)
		self.transport.release (_connection)
		self._status = "executed"
		self._transcript.internal (0x21a65363, "executed;")
	
	
	def _execute_connect (self) :
		
		_connection = self.transport.connect (self.request.server_endpoint, self.request.server_tls)
		
		return _connection
	
	
	def _execute_request (self, _connection) :
		
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
		
		_transcript = self._transcript.fork ()
		
		if self.request.host is not None :
			_transcript.internal (0x02551cf9, "host: `%s`;", self.request.host)
		for _name, _value in _headers :
			_transcript.internal (0x02551cf9, "header `%s`: `%s`;", _name, _value)
		if self.request.body is not None :
			_transcript.internal (0x02551cf9, "body: `%d`;", len (self.request.body))
		
		# NOTE:  _connection.request (self.request.method, _selector, self.request.body, _headers)
		
		_connection.putrequest (self.request.method, _selector, True, True)
		
		for _name, _value in _headers :
			if _name.lower () == "content-length" :
				raise Exception (0xb9234238)
			_connection.putheader (_name, _value)
		if self.request.body is not None :
			_connection.putheader ("Content-Length", str (len (self.request.body)))
		elif self.request.method not in ["GET", "HEAD"] :
			_connection.putheader ("Content-Length", "0")
		_connection.endheaders ()
		
		if self.request.body is not None :
			_connection.send (self.request.body)
		else :
			_connection.send ("")
	
	
	def _execute_response (self, _connection) :
		
		self._transcript.debug (0x9e154782, "receiving response...")
		
		_response = _connection.getresponse ()
		
		_status_code = _response.status
		_status_version = _response.version
		_status_message = _response.reason
		
		if _status_version == 10 :
			_status_version = "1.0"
		elif _status_version == 11 :
			_status_version = "1.1"
		else :
			raise Exception (0xcb3ab75e)
		
		_transcript = self._transcript.fork ()
		
		_transcript.internal (0xa6fcadaf, "status: `%s`;", _status_code)
		_transcript.internal (0x92172b62, "version: `%s`;", _status_version)
		_transcript.internal (0x29813ff7, "message: `%s`;", _status_message)
		
		_headers = list ()
		for _name, _value in _response.getheaders () :
			_transcript.internal (0x3ed4ed10, "header `%s`: `%s`;", _name, _value)
			_headers.append ((_name, _value))
		
		_body = _response.read ()
		if len (_body) == 0 :
			_body = None
		
		if _body is not None :
			_transcript.internal (0xffe8cfb6, "body: `%d`;", len (_body))
		
		self.response = Response (_status_code, _status_version, _status_message, _headers, _body)
	
	
	def _trace (self, _tracer, _annotations = True) :
		
		if _annotations :
			if len (self.annotations._records) > 0 :
				_tracer (0x08574ba6, "* annotations:")
				_tracer_annotations = _tracer.fork ()
				for _record in self.annotations._records :
					if _record.levelname == "ERROR" or _record.levelname == "CRITICAL" :
						_prefix = "!!!! "
					elif _record.levelname == "WARNING" :
						_prefix = "[ww] "
					elif _record.levelname == "INFO" or _record.levelname == "NOTICE" :
						_prefix = "[ii] "
					elif _record.levelname == "DEBUG" :
						_prefix = "[dd] "
					else :
						_prefix = "[??] [%-6.6s] " % (_record.levelname,)
					_tracer_annotations (0xcb6c9a7b, _prefix + _record.msg, *_record.args)
			else :
				_tracer (0x0c31f78c, "* annotations: none;")
		
		if self.request is not None :
			_tracer (0xa21095ed, "* request:")
			self.request._trace (_tracer.fork ())
		else :
			_tracer (0xbce1112c, "* request: none;")
		
		if self.response is not None :
			_tracer (0x80d7ba56, "* response:")
			self.response._trace (_tracer.fork ())
		else :
			_tracer (0x1c59088d, "* response: none;")




class Transport (object) :
	
	
	def __init__ (self, _context) :
		self._context = _context
		self._transcript = transcript (self, 0xb497f562)
		self._connections_pool = dict ()
		self._mutex = threading.Lock ()
	
	
	def connect (self, _endpoint, _tls) :
		
		_key = (_endpoint, _tls)
		_connection = None
		
		with self._mutex :
			if _key in self._connections_pool :
				_connections = self._connections_pool[_key]
				if len (_connections) > 0 :
					_connection = _connections.pop ()
		
		if _connection is not None :
			if (time.time () - _connection.____httt_timestamp) <= 6 :
				self._transcript.debug (0x3a3b0c4d, "reusing connection to `%s` with TLS `%s`;", _endpoint, _tls)
				_connection.____httt_counter += 1
				return _connection
		
		self._transcript.debug (0x95adb4dd, "connecting to `%s` with TLS `%s`...", _endpoint, _tls)
		
		if _tls :
			_ssl = ssl._create_unverified_context ()
			_connection = httplib.HTTPSConnection (
					host = _endpoint,
					strict = True,
					timeout = 30,
					context = _ssl,
				)
		else :
			_connection = httplib.HTTPConnection (
					host = _endpoint,
					strict = True,
					timeout = 30,
				)
		
		_connection.connect ()
		
		_connection.____httt_key = _key
		_connection.____httt_counter = 1
		
		return _connection
	
	
	def release (self, _connection) :
		
		if _connection.____httt_counter >= 64 :
			_connection.close ()
			return
		
		_connection.____httt_timestamp = time.time ()
		
		_key = _connection.____httt_key
		
		with self._mutex :
			if _key not in self._connections_pool :
				self._connections_pool[_key] = [_connection]
			else :
				self._connections_pool[_key].append (_connection)

