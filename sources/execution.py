

from http import *
import tests # recursive-import
from transcript import *




class Execution (object) :
	
	
	def __init__ (self, _context) :
		self._context = _context
		self._transcript = transcript (self, 0x332ac851)
		self._transactions = list ()
	
	
	def execute (self, _test) :
		self._transcript.trace (0x91657e21, "executing...")
		self._execute (_test, ())
		if len (self._transactions) == 0 :
			self._transcript.info (0xc5327e15, "execution yielded no transactions!")
		self._transcript.trace (0x310eac5e, "executed;")
	
	
	def _execute (self, _test, _stack) :
		if isinstance (_test, tests.Test) :
			self._execute_test (_test, _stack)
		elif isinstance (_test, tests.Tests) :
			self._execute_tests (_test, _stack)
		else :
			raise Exception (0xbe83caa9)
	
	
	def _execute_tests (self, _tests, _stack) :
		_stack = _stack + (_tests.identifier,)
		_identifier = " -- ".join (_stack)
		self._transcript.debug (0xe605026e, "beginning `%s`...", _identifier)
		for _test in _tests._tests :
			self._execute (_test, _stack)
		self._transcript.trace (0xd6ef2184, "finished `%s`;", _identifier)
	
	
	def _execute_test (self, _test, _stack) :
		_stack = _stack + (_test.identifier,)
		_identifier = " -- ".join (_stack)
		self._transcript.info (0xe6c0c539, "executing `%s`...", _identifier)
		
		_session = Session ()
		_transaction = Transaction (self._context, _session, _test._request_builder, _test._response_enforcer)
		_transaction.prepare ()
		_transaction.execute ()
		_succeeded = _transaction.enforce ()
		
		self._transactions.append (_transaction)
		
		if _succeeded :
			self._transcript.debug (0x9541c9ec, "succeeded executing `%s`;", _identifier)
		else :
			self._transcript.error (0x78f26ad5, "failed executing `%s`!", _identifier)
		
		if len (_transaction.annotations._records) > 0 :
			self._transcript.debug (0xbf5f42ac, "annotations:")
			_transaction.annotations._propagate (self._transcript)
		
		self._transcript.trace (0x4b83e138, "executed `%s`;", _identifier)
	
	
	def _trace (self, _tracer) :
		if len (self._transactions) > 0 :
			_tracer (0xc0a5f644, "* transactions:")
			for _transaction in self._transactions :
				_transaction._trace (_tracer)
		else :
			_tracer (0x1cd6ab66, "* transactions: none;")
	
	def _dump (self) :
		self._trace (dump)

