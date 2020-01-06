

from crypto import *
from http import *
import tests # recursive-import
from transcript import *




class Execution (object) :
	
	
	def __init__ (self, _context, _hooks = None) :
		self._context = _context
		self._hooks = _hooks
		self._transcript = transcript (self, 0x332ac851)
		self._transport = Transport (self._context)
		self._transactions = list ()
		self._transactions_by_handle = dict ()
		self._statistics = ExecutionStatistics ()
		self._statistics._aggregated = dict ()
		self._debug = None
	
	
	def execute (self, _test, _debug = None) :
		self._transcript.cut ()
		self._transcript.internal (0x91657e21, "executing...")
		_debug = self._debug if _debug is None else _debug
		self._execute (_test, None, None, self._debug)
		self._transcript.internal (0x310eac5e, "executed;")
		self._transcript.cut ()
		self._report_execution (_debug)
	
	
	def _execute (self, _test, _tests_stack, _identifier_stack, _debug) :
		if isinstance (_test, tests.Test) :
			self._execute_test (_test, _tests_stack, _identifier_stack, _debug)
		elif isinstance (_test, tests.Tests) :
			self._execute_tests (_test, _tests_stack, _identifier_stack, _debug)
		else :
			raise Exception (0xbe83caa9)
		self._report_progress (_debug)
	
	
	def _execute_tests (self, _tests, _tests_stack, _identifier_stack, _debug) :
		
		_tests_stack = (_tests_stack, _tests)
		_identifier_stack = (_identifier_stack, _tests.identifier)
		_identifier = stringify_identifier (_identifier_stack)
		_handle = fingerprint (_identifier_stack)
		
		if self._hooks is not None and not self._hooks.should_execute_tests (_handle, _identifier, _tests) :
			self._transcript.debug (0x94dc4cef, "skipping [%s] `%s`...", _handle, _identifier)
			return
		
		_debug = _tests._debug if _debug is None else _debug
		self._transcript.debug (0xe605026e, "beginning [%s] `%s`...", _handle, _identifier)
		
		if _tests_stack[0] is None :
			_statistics = self._statistics
		else :
			_statistics = _tests_stack[0][1]._statistics
		if _tests.identifier in _statistics._aggregated :
			_statistics = _statistics._aggregated[_tests.identifier]
		else :
			_statistics._aggregated[_tests.identifier] = ExecutionStatistics ()
			_statistics = _statistics._aggregated[_tests.identifier]
			_statistics._identifier = _tests.identifier
			_statistics._aggregated = dict ()
		
		_tests._statistics = _statistics
		
		for _test in _tests._tests :
			self._execute (_test, _tests_stack, _identifier_stack, _debug)
		
		if _tests._statistics.succeeded :
			self._transcript.internal (0xd6ef2184, "finished [%s] `%s`;", _handle, _identifier)
		else :
			self._transcript.notice (0xd5081953, "finished [%s] `%s`:  %d executed;  %d (%.0f%%) failed;", _handle, _identifier, _tests._statistics.count_executed, _tests._statistics.count_failed, _tests._statistics.ratio_failed * 100)
	
	
	def _execute_test (self, _test, _tests_stack, _identifier_stack, _debug) :
		
		_identifier_stack = (_identifier_stack, _test.identifier)
		_identifier = stringify_identifier (_identifier_stack)
		_handle = fingerprint (_identifier_stack)
		
		if _handle in self._transactions_by_handle :
			self._transcript.error (0x0472ccf3, "duplicate [%s] `%s`;  ignoring!", _handle, _identifier)
			return
		
		if self._hooks is not None and not self._hooks.should_execute_test (_handle, _identifier, _test) :
			self._transcript.debug (0xe3195455, "skipping [%s] `%s`...", _handle, _identifier)
			return
		
		_debug = _test._debug if _debug is None else _debug
		self._transcript.cut ()
		self._transcript.info (0xe6c0c539, "executing [%s] `%s`...", _handle, _identifier)
		
		_session = Session ()
		_transaction = Transaction (self._context, self._transport, _session, _test.requests, _test.responses)
		
		if self._hooks is not None :
			self._hooks.before_prepare_test (_handle, _identifier, _test, _transaction)
		
		_transaction.prepare ()
		
		if self._hooks is not None :
			self._hooks.after_prepare_test (_handle, _identifier, _test, _transaction)
		
		if self._hooks is not None :
			self._hooks.before_execute_test (_handle, _identifier, _test, _transaction)
		
		_transaction.execute ()
		
		if self._hooks is not None :
			self._hooks.after_execute_test (_handle, _identifier, _test, _transaction)
		
		if self._hooks is not None :
			self._hooks.before_enforce_test (_handle, _identifier, _test, _transaction)
		
		_succeeded = _transaction.enforce ()
		
		if self._hooks is not None :
			self._hooks.after_enforce_test (_handle, _identifier, _test, _transaction)
		
		self._transactions.append ((_handle, _identifier, _transaction))
		self._transactions_by_handle[_handle] = _transaction
		
		if _succeeded :
			
			if self._hooks is not None :
				self._hooks.succeeded_test (_handle, _identifier, _test, _transaction)
			
			self._transcript.debug (0x9541c9ec, "succeeded executing [%s];", _handle)
			
		else :
			
			if self._hooks is not None :
				self._hooks.failed_test (_handle, _identifier, _test, _transaction)
			
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
		
		_transaction.sanitize ()
		
		self._transcript.internal (0x4b83e138, "executed [%s];", _handle)
		self._transcript.cut ()
		
		self._update_statistics (_tests_stack, _transaction)
	
	
	def _update_statistics (self, _tests_stack, _transaction) :
		
		while _tests_stack is not None :
			_tests_stack[1]._statistics._update (_transaction)
			_tests_stack = _tests_stack[0]
		
		self._statistics._update (_transaction)
	
	
	def _report_progress (self, _debug) :
		
		if not _debug and (self._statistics.count_executed % 10) != 0 or self._statistics.count_executed == 0 :
			return
		
		self._transcript.cut ()
		self._transcript.notice (0xe8e97c33, "execution progress:  %d executed;  %d (%.0f%%) failed;", self._statistics.count_executed, self._statistics.count_failed, self._statistics.ratio_failed * 100)
		self._transcript.cut ()
	
	
	def _report_execution (self, _debug) :
		self._transcript.cut ()
		
		if len (self._transactions) > 0 :
			if self._statistics.succeeded :
				self._transcript.notice (0xd23fd5de, "execution outcome:  %d executed;  all succeeded;", self._statistics.count_executed)
			else :
				self._transcript.warning (0xe8e97c33, "execution outcome:  %d executed;  %d (%.0f%%) failed;", self._statistics.count_executed, self._statistics.count_failed, self._statistics.ratio_failed * 100)
		else :
			self._transcript.warning (0xc5327e15, "execution yielded no transactions!")
		
		def _report_statistics (_statistics, _transcript, _only_aggregated = False) :
			
			if not _only_aggregated :
				_identifier = stringify_identifier (_statistics._identifier)
				if _statistics.succeeded :
					_transcript.info (0x9742017c, "`%s`:  %d executed;  all succeeded;", _identifier, _statistics.count_executed)
				else :
					_transcript.info (0x6c5fcc49, "`%s`:  %d executed;  %d (%.0f%%) failed;", _identifier, _statistics.count_executed, _statistics.count_failed, _statistics.ratio_failed * 100)
				_transcript = _transcript.fork ()
			
			for _identifier, _statistics in sorted (_statistics._aggregated.iteritems ()) :
				if _statistics.count_executed > 0 :
					_report_statistics (_statistics, _transcript.fork (False))
		
		_report_statistics (self._statistics, self._transcript.fork (), True)
		
		self._transcript.cut ()
	
	
	def _trace (self, _tracer) :
		
		if len (self._transactions) > 0 :
			
			_tracer_meta = _tracer.fork (False)
			_tracer_meta.cut ()
			_tracer_meta (0x00de4d05, "## statistics:")
			_tracer_meta.indent ()
			_tracer_meta (0x5cfb4baa, "executed total: %d;", self._statistics.count_executed)
			_tracer_meta (0x5c414e7e, "executed succeeded: %d (%.0f%%);", self._statistics.count_succeeded, self._statistics.ratio_succeeded * 100)
			_tracer_meta (0x3fc6ecdc, "executed failed: %d (%.0f%%);", self._statistics.count_failed, self._statistics.ratio_failed * 100)
			_tracer_meta.cut ()
			
			
			_tracer_meta = _tracer.fork (False)
			_tracer_meta.cut ()
			_tracer_meta (0x84cb7e16, "## tests:")
			
			def _report_statistics (_statistics, _tracer, _only_aggregated = False) :
				
				if not _only_aggregated :
					_identifier = stringify_identifier (_statistics._identifier)
					if _statistics.succeeded :
						_tracer (0xcbac6bd3, "`%s`:  %d executed;  all succeeded;", _identifier, _statistics.count_executed)
					else :
						_tracer (0xa1fc227b, "`%s`:  %d executed;  %d (%.0f%%) failed;", _identifier, _statistics.count_executed, _statistics.count_failed, _statistics.ratio_failed * 100)
					_tracer = _tracer.fork ()
				
				for _identifier, _statistics in sorted (_statistics._aggregated.iteritems ()) :
					if _statistics.count_executed > 0 :
						_report_statistics (_statistics, _tracer.fork (False))
			
			_report_statistics (self._statistics, _tracer_meta.fork (), True)
			_tracer_meta.cut ()
			
			
			for _identifier, _handle, _transaction in sorted (self._transactions) :
				_succeeded = _transaction.succeeded
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




class ExecutionStatistics (object) :
	
	
	def __init__ (self) :
		
		self.succeeded = True
		
		self.count_executed = 0
		self.count_succeeded = 0
		self.count_failed = 0
	
	
	def _update (self, _transaction) :
		
		self.count_executed += 1
		if _transaction.succeeded :
			self.count_succeeded += 1
		else :
			self.count_failed += 1
			self.succeeded = False
		
		self.ratio_succeeded = float (self.count_succeeded) / self.count_executed
		self.ratio_failed = float (self.count_failed) / self.count_executed




class ExecutionHooks (object) :
	
	def __init__ (self) :
		pass
	
	
	def should_execute_tests (self, _handle, _identifier, _tests) :
		return self.should_execute (_handle)
	
	def should_execute_test (self, _handle, _identifier, _test) :
		return self.should_execute (_handle)
	
	def should_execute (self, _handle) :
		return True
	
	
	def before_prepare_test (self, _handle, _identifier, _test, _transaction) :
		pass
	
	def after_prepare_test (self, _handle, _identifier, _test, _transaction) :
		pass
	
	
	def before_execute_test (self, _handle, _identifier, _test, _transaction) :
		pass
	
	def after_execute_test (self, _handle, _identifier, _test, _transaction) :
		pass
	
	
	def before_enforce_test (self, _handle, _identifier, _test, _transaction) :
		pass
	
	def after_enforce_test (self, _handle, _identifier, _test, _transaction) :
		pass
	
	
	def succeeded_test (self, _handle, _identifier, _test, _transaction) :
		pass
	
	def failed_test (self, _handle, _identifier, _test, _transaction) :
		pass

