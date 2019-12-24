

from crypto import *
from http import *
import tests # recursive-import
from transcript import *




class Execution (object) :
	
	
	def __init__ (self, _context) :
		self._context = _context
		self._transcript = transcript (self, 0x332ac851)
		self._transport = Transport (self._context)
		self._transactions = list ()
		self._transactions_by_handle = dict ()
		self._debug = None
	
	
	def execute (self, _test, _debug = None) :
		self._transcript.cut ()
		self._transcript.internal (0x91657e21, "executing...")
		_debug = self._debug if _debug is None else _debug
		self._execute (_test, (), self._debug)
		if len (self._transactions) == 0 :
			self._transcript.info (0xc5327e15, "execution yielded no transactions!")
		self._transcript.internal (0x310eac5e, "executed;")
		self._transcript.cut ()
	
	
	def _execute (self, _test, _stack, _debug) :
		if isinstance (_test, tests.Test) :
			self._execute_test (_test, _stack, _debug)
		elif isinstance (_test, tests.Tests) :
			self._execute_tests (_test, _stack, _debug)
		else :
			raise Exception (0xbe83caa9)
	
	
	def _execute_tests (self, _tests, _stack, _debug) :
		
		_stack = (_stack, _tests.identifier)
		_identifier = stringify_identifier (_stack)
		_handle = fingerprint (_stack)
		
		_debug = _tests._debug if _debug is None else _debug
		self._transcript.debug (0xe605026e, "beginning [%s] `%s`...", _handle, _identifier)
		
		for _test in _tests._tests :
			self._execute (_test, _stack, _debug)
		
		self._transcript.internal (0xd6ef2184, "finished [%s];", _handle)
	
	
	def _execute_test (self, _test, _stack, _debug) :
		
		_stack = (_stack, _test.identifier)
		_identifier = stringify_identifier (_stack)
		_handle = fingerprint (_stack)
		
		if _handle in self._transactions_by_handle :
			self._transcript.error (0x0472ccf3, "duplicate [%s] `%s`;  ignoring!", _handle, _identifier)
			return
		
		_debug = _test._debug if _debug is None else _debug
		self._transcript.cut ()
		self._transcript.info (0xe6c0c539, "executing [%s] `%s`...", _handle, _identifier)
		
		_session = Session ()
		_transaction = Transaction (self._context, self._transport, _session, _test.requests, _test.responses)
		_transaction.prepare ()
		_transaction.execute ()
		_succeeded = _transaction.enforce ()
		
		self._transactions.append ((_handle, _identifier, _transaction, _succeeded))
		self._transactions_by_handle[_handle] = _transaction
		
		if _succeeded :
			self._transcript.debug (0x9541c9ec, "succeeded executing [%s];", _handle)
		else :
			self._transcript.error (0x78f26ad5, "failed executing [%s] `%s`!", _handle, _identifier)
		
		if len (_transaction.annotations._records) > 0 :
			self._transcript.debug (0xbf5f42ac, "annotations:")
			_transaction.annotations._propagate (self._transcript.fork ())
		
		if not _succeeded :
			if _debug :
				self._transcript.warning (0x9867da91, "transaction:")
				_transaction._trace (self._transcript.warning_tracer (True), False)
			else :
				self._transcript.debug (0xbcabaeab, "transaction:")
				_transaction._trace (self._transcript.debug_tracer (True), False)
		elif _debug :
			self._transcript.info (0x4a616c55, "transaction:")
			_transaction._trace (self._transcript.info_tracer (True), True)
		
		self._transcript.internal (0x4b83e138, "executed [%s];", _handle)
		self._transcript.cut ()
	
	
	def _trace (self, _tracer) :
		if len (self._transactions) > 0 :
			for _identifier, _handle, _transaction, _succeeded in sorted (self._transactions) :
				_tracer.cut ()
				if not _succeeded :
					_tracer (0xb86f3e97, "!!!! FAILED !!!!")
				_tracer_meta = _tracer.fork (False)
				_tracer_meta (0xc0a5f644, "## transaction:")
				_tracer_meta.indent ()
				_tracer_meta (0x67181c6a, "* meta:")
				_tracer_meta.indent ()
				if _succeeded :
					_tracer_meta (0x3191db36, "outcome: succeeded;")
				else :
					_tracer_meta (0x2264995e, "outcome: failed;")
				_tracer_meta (0x2d836357, "identifier: `%s`;", _identifier)
				_tracer_meta (0xdb41b7d9, "handle: `%s`;", _handle)
				_tracer_meta.indent (-1)
				_transaction._trace (_tracer_meta, True)
				if not _succeeded :
					_tracer (0x14aaf57d, "!!!! FAILED !!!!")
				_tracer.cut ()
		else :
			_tracer (0x1cd6ab66, "## transactions: none;")
	
	
	def dump (self, _stream = None) :
		_tracer = dumper (_stream)
		self._trace (_tracer)

