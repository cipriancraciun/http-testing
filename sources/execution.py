

from http import *
import tests # recursive-import
from transcript import *




class Execution (object) :
	
	
	def __init__ (self, _context) :
		self._context = _context
		self._transcript = transcript (self, 0x332ac851)
	
	
	def execute (self, _test) :
		self._transcript.trace (0x91657e21, "executing...")
		self._execute (_test, ())
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
		_identifier = " / ".join (_stack)
		self._transcript.debug (0xe605026e, "beginning `%s`...", _identifier)
		for _test in _tests._tests :
			self._execute (_test, _stack)
		self._transcript.trace (0xd6ef2184, "finished `%s`;", _identifier)
	
	
	def _execute_test (self, _test, _stack) :
		_stack = _stack + (_test.identifier,)
		_identifier = " / ".join (_stack)
		self._transcript.info (0xe6c0c539, "executing `%s`...", _identifier)
		
		_session = Session ()
		_transaction = Transaction (self._context, _session, _test._request_builder, _test._response_enforcer)
		_transaction.prepare ()
		_transaction.execute ()
		_succeeded = _transaction.enforce ()
		
		if _succeeded :
			self._transcript.debug (0x9541c9ec, "succeeded executing `%s`;", _identifier)
		else :
			self._transcript.error (0x78f26ad5, "failed executing `%s`!", _identifier)
		
		if len (_transaction.annotations._records) > 0 :
			for _record in _transaction.annotations._records :
				self._transcript.warning (0xa1056f0f, "-> %s", _record.getMessage ())
		
		self._transcript.trace (0x4b83e138, "executed `%s`;", _identifier)

