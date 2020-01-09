

import Queue as queue
import threading

from crypto import *
from http import *
import tests # recursive-import
from transcript import *




class Executor (object) :
	
	
	def __init__ (self, _context, _transport = None, _hooks = None, _parallelism = None, _debug = None) :
		
		if _transport is None :
			_transport = Transport (_context)
		
		self._context = _context
		self._transport = _transport
		self._hooks = _hooks
		self._parallelism = _parallelism
		self._debug = _debug
		
		self._transcript = transcript (self, 0x332ac851)
	
	
	def execute (self, _test) :
		
		_plan = ExecutionPlan (self._context, self._transport, self._hooks, self._parallelism, self._debug)
		
		self._transcript.cut ()
		self._transcript.notice (0x8d8c3f01, "planning...")
		
		self._plan (_plan, _test, None, None, _plan._debug, False)
		
		_plan._tasks = list ()
		for _identifier, _task in sorted (_plan._tasks_by_identifier.iteritems ()) :
			_plan._tasks.append (_task)
		
		self._transcript.debug (0xa4b3290e, "planned;")
		self._transcript.cut ()
		
		self._transcript.cut ()
		self._transcript.debug (0x91657e21, "executing...")
		
		self._execute_plan (_plan)
		
		self._transcript.debug (0x310eac5e, "executed;")
		self._transcript.cut ()
		
		_plan._report_execution ()
		
		return _plan
	
	
	def _plan (self, _plan, _test, _identifier_stack, _statistics_stack, _debug, _skip) :
		if isinstance (_test, tests.Test) :
			self._plan_test (_plan, _test, _identifier_stack, _statistics_stack, _debug, _skip)
		elif isinstance (_test, tests.Tests) :
			self._plan_tests (_plan, _test, _identifier_stack, _statistics_stack, _debug, _skip)
		else :
			raise Exception (0xbe83caa9)
	
	
	def _plan_tests (self, _plan, _tests, _identifier_stack, _statistics_stack, _debug, _skip) :
		
		_identifier_stack = (_identifier_stack, _tests.identifier)
		_identifier = stringify_identifier (_identifier_stack)
		_handle = fingerprint (_identifier_stack)
		
		if _statistics_stack is None :
			_statistics_stack = (None, _plan._statistics)
		_statistics = _statistics_stack[1]
		
		if _tests.identifier in _statistics._aggregated :
			_statistics = _statistics._aggregated[_tests.identifier]
		else :
			_statistics._aggregated[_tests.identifier] = ExecutionStatistics ()
			_statistics = _statistics._aggregated[_tests.identifier]
			_statistics._identifier = _tests.identifier
			_statistics._aggregated = dict ()
		
		_statistics_stack = (_statistics_stack, _statistics)
		
		_debug = _tests._debug if _debug is None else _debug
		
		self._transcript.debug (0xe605026e, "planning [%s] `%s`...", _handle, _identifier)
		
		if _skip or _tests._skip or _plan._hooks is not None and not _plan._hooks.should_execute_tests (_handle, _identifier, _tests) :
			self._transcript.debug (0x94dc4cef, "skipping [%s] `%s`...", _handle, _identifier)
			_skip = True
		
		for _test in _tests._tests :
			self._plan (_plan, _test, _identifier_stack, _statistics_stack, _debug, _skip)
		
		self._transcript.debug (0x16de40be, "planned [%s] `%s`;", _handle, _identifier)
	
	
	def _plan_test (self, _plan, _test, _identifier_stack, _statistics_stack, _debug, _skip) :
		
		_identifier_stack = (_identifier_stack, _test.identifier)
		_identifier = stringify_identifier (_identifier_stack)
		_enforcer_handle = _test.responses.fingerprint ()
		_handle = fingerprint ((_identifier_stack, _enforcer_handle))
		
		_debug = _test._debug if _debug is None else _debug
		
		if _handle in _plan._tasks_by_handle :
			self._transcript.warning (0x0472ccf3, "duplicate [%s] `%s`;  ignoring!", _handle, _identifier)
			return
		
		if _skip or _test._skip or _plan._hooks is not None and not _plan._hooks.should_execute_test (_handle, _identifier, _test) :
			self._transcript.debug (0xe3195455, "skipping [%s] `%s`...", _handle, _identifier)
			self._update_statistics (_statistics_stack, False)
			return
		
		_session = Session ()
		_transaction = Transaction (_plan._context, _plan._transport, _session, _test.requests, _test.responses)
		_task = ExecutionTask (_handle, _identifier, _test, _transaction, _enforcer_handle, _statistics_stack, _debug)
		
		_plan._enqueue_task (_task)
		self._update_statistics (_statistics_stack, True)
	
	
	def _execute_plan (self, _plan) :
		
		if len (_plan._tasks) > 0 :
			if _plan._parallelism > 1 :
				self._execute_plan_parallelized (_plan)
			else :
				self._execute_plan_sequentially (_plan)
	
	
	def _execute_plan_sequentially (self, _plan) :
		
		self._transcript.notice (0xa32bd88a, "executing sequentially...")
		
		for _task in _plan._tasks :
			
			self._execute_task_before (_task._handle, _task._identifier, _task._transaction, _plan, _task._test, _task._debug)
			self._execute_task_actual (_task._handle, _task._identifier, _task._transaction, _plan, _task._test, _task._debug)
			self._execute_task_after (_task._handle, _task._identifier, _task._transaction, _plan, _task._test, _task._debug)
			
			_plan._report_progress ()
	
	
	def _execute_plan_parallelized (self, _plan) :
		
		self._transcript.notice (0x0ee7d23b, "executing parallelized (%d)...", _plan._parallelism)
		
		_parallelism_threads = _plan._parallelism
		_parallelism_queue = _parallelism_threads * 4
		_pending_queue = queue.Queue (_parallelism_queue)
		_executed_queue = queue.Queue (_parallelism_queue)
		
		def _execute_actual () :
			while True :
				_task = _pending_queue.get ()
				if _task is None :
					break
				self._execute_task_actual (_task._handle, _task._identifier, _task._transaction, _plan, _task._test, _task._debug)
				_executed_queue.put (_task)
		
		_threads = list ()
		for _index in xrange (_parallelism_threads) :
			_thread = threading.Thread (target = _execute_actual)
			_thread.daemon = True
			_thread.start ()
		
		_tasks_queue = list (_plan._tasks)
		_tasks_expected = len (_tasks_queue)
		
		while True :
			
			if _tasks_expected == 0 :
				break
			
			while len (_tasks_queue) > 0 and not _pending_queue.full () :
				_task = _tasks_queue.pop ()
				self._execute_task_before (_task._handle, _task._identifier, _task._transaction, _plan, _task._test, _task._debug)
				_pending_queue.put (_task)
			
			while True :
				_task = _executed_queue.get ()
				_tasks_expected -= 1
				self._execute_task_after (_task._handle, _task._identifier, _task._transaction, _plan, _task._test, _task._debug)
				self._update_statistics (_task._statistics_stack, _task._transaction)
				if _executed_queue.empty () :
					break
			
			_plan._report_progress ()
		
		for _index in xrange (_parallelism_threads) :
			_pending_queue.put (None)
		for _thread in _threads :
			_thread.join ()
	
	
	def _execute_task_before (self, _handle, _identifier, _transaction, _plan, _test, _debug) :
		
		self._transcript.cut ()
		self._transcript.debug (0xe6c0c539, "executing [%s] `%s`...", _handle, _identifier)
		
		if _plan._hooks is not None :
			_plan._hooks.before_prepare_test (_handle, _identifier, _test, _transaction)
		
		_transaction.prepare ()
		
		if _plan._hooks is not None :
			_plan._hooks.after_prepare_test (_handle, _identifier, _test, _transaction)
		
		if _plan._hooks is not None :
			_plan._hooks.before_execute_test (_handle, _identifier, _test, _transaction)
	
	
	def _execute_task_actual (self, _handle, _identifier, _transaction, _plan, _test, _debug) :
		
		_transaction.execute ()
	
	
	def _execute_task_after (self, _handle, _identifier, _transaction, _plan, _test, _debug) :
		
		if _plan._hooks is not None :
			_plan._hooks.after_execute_test (_handle, _identifier, _test, _transaction)
		
		if _plan._hooks is not None :
			_plan._hooks.before_enforce_test (_handle, _identifier, _test, _transaction)
		
		_succeeded = _transaction.enforce ()
		
		if _plan._hooks is not None :
			_plan._hooks.after_enforce_test (_handle, _identifier, _test, _transaction)
		
		if _succeeded :
			
			if _plan._hooks is not None :
				_plan._hooks.succeeded_test (_handle, _identifier, _test, _transaction)
			
			self._transcript.debug (0x9541c9ec, "succeeded executing [%s];", _handle)
			
		else :
			
			if _plan._hooks is not None :
				_plan._hooks.failed_test (_handle, _identifier, _test, _transaction)
			
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
		
		self._transcript.debug (0x4b83e138, "executed [%s];", _handle)
		self._transcript.cut ()
	
	
	def _update_statistics (self, _statistics_stack, _transaction) :
		
		while _statistics_stack is not None :
			
			if _transaction is True :
				_statistics_stack[1]._update_planned ()
			elif _transaction is False :
				_statistics_stack[1]._update_skipped ()
			else :
				_statistics_stack[1]._update_executed (_transaction)
			
			_statistics_stack = _statistics_stack[0]




class ExecutionTask (object) :
	
	def __init__ (self, _handle, _identifier, _test, _transaction, _enforcer_handle, _statistics_stack, _debug) :
		self._handle = _handle
		self._identifier = _identifier
		self._test = _test
		self._transaction = _transaction
		self._enforcer_handle = _enforcer_handle
		self._statistics_stack = _statistics_stack
		self._debug = _debug




class ExecutionPlan (object) :
	
	def __init__ (self, _context, _transport, _hooks, _parallelism, _debug) :
		
		if _parallelism is None :
			_parallelism = True
		
		if _parallelism is False :
			_parallelism = 1
		elif _parallelism is True :
			_parallelism = 64
		elif isinstance (_parallelism, int) and _parallelism >= 1 :
			pass
		else :
			raise Exception (0xf248be6c)
		
		self._context = _context
		self._transport = _transport
		self._hooks = _hooks
		self._parallelism = _parallelism
		self._debug = _debug
		
		self._transcript = transcript (self, 0xcc4f6cd1)
		
		self._tasks = list ()
		self._tasks_by_handle = dict ()
		self._tasks_by_identifier = dict ()
		
		self._statistics = ExecutionStatistics ()
		self._statistics._aggregated = dict ()
		
		self._report_progress_last_count_executed = 0
	
	
	def _enqueue_task (self, _task) :
		
		self._tasks.append (_task)
		self._tasks_by_handle[_task._handle] = _task
		self._tasks_by_identifier[_task._identifier] = _task
	
	
	def _report_progress (self) :
		
		if not self._debug and (self._statistics.count_executed - self._report_progress_last_count_executed) < 10 :
			return
		
		self._report_progress_last_count_executed = self._statistics.count_executed
		
		self._transcript.cut ()
		self._transcript.notice (0xe8e97c33, "execution progress:  %d (%.0f%%) executed;  %d (%.0f%%) failed;  %d planned;  %d skipped;", self._statistics.count_executed, self._statistics.ratio_executed * 100, self._statistics.count_failed, self._statistics.ratio_failed * 100, self._statistics.count_planned, self._statistics.count_skipped)
		self._transcript.cut ()
	
	
	def _report_execution (self) :
		self._transcript.cut ()
		
		if self._statistics.count_executed > 0 :
			if self._statistics.succeeded :
				self._transcript.notice (0xd23fd5de, "execution outcome:  %d executed;  %d skipped;  all succeeded;", self._statistics.count_executed, self._statistics.count_skipped)
			else :
				self._transcript.warning (0xe8e97c33, "execution outcome:  %d executed;  %d (%.0f%%) failed;  %d skipped;", self._statistics.count_executed, self._statistics.count_failed, self._statistics.ratio_failed * 100, self._statistics.count_skipped)
		else :
			self._transcript.warning (0xc5327e15, "execution yielded no transactions!")
		
		def _report_statistics (_statistics, _transcript, _only_aggregated = False) :
			
			if not _only_aggregated :
				_identifier = stringify_identifier (_statistics._identifier)
				if _statistics.succeeded :
					_transcript.info (0x9742017c, "`%s`:  %d executed;  %d skipped;  all succeeded;", _identifier, _statistics.count_executed, _statistics.count_skipped)
				else :
					_transcript.warning (0x6c5fcc49, "`%s`:  %d executed;  %d (%.0f%%) failed;  %d skipped;", _identifier, _statistics.count_executed, _statistics.count_failed, _statistics.ratio_failed * 100, _statistics.count_skipped)
				_transcript = _transcript.fork ()
			
			for _identifier, _statistics in sorted (_statistics._aggregated.iteritems ()) :
				if _statistics.count_total > 0 :
					_report_statistics (_statistics, _transcript.fork (False))
		
		_report_statistics (self._statistics, self._transcript.fork (), True)
		
		self._transcript.cut ()
	
	
	def _trace (self, _tracer) :
		
		if len (self._tasks) > 0 :
			
			_tracer_meta = _tracer.fork (False)
			_tracer_meta.cut ()
			_tracer_meta (0x00de4d05, "## statistics:")
			_tracer_meta.indent ()
			_tracer_meta (0x5cfb4baa, "executed total: %d;", self._statistics.count_executed)
			_tracer_meta (0x5c414e7e, "executed succeeded: %d (%.0f%%);", self._statistics.count_succeeded, self._statistics.ratio_succeeded * 100)
			_tracer_meta (0x3fc6ecdc, "executed failed: %d (%.0f%%);", self._statistics.count_failed, self._statistics.ratio_failed * 100)
			_tracer_meta (0x5cfb4baa, "skipped: %d;", self._statistics.count_skipped)
			_tracer_meta.cut ()
			
			
			_tracer_meta = _tracer.fork (False)
			_tracer_meta.cut ()
			_tracer_meta (0x84cb7e16, "## tests:")
			
			def _report_statistics (_statistics, _tracer, _only_aggregated = False) :
				
				if not _only_aggregated :
					_identifier = stringify_identifier (_statistics._identifier)
					if _statistics.succeeded :
						_tracer (0xcbac6bd3, "`%s`:  %d executed;  %d skipped;  all succeeded;", _identifier, _statistics.count_executed, _statistics.count_skipped)
					else :
						_tracer (0xa1fc227b, "`%s`:  %d executed;  %d (%.0f%%) failed;  %d skipped;", _identifier, _statistics.count_executed, _statistics.count_failed, _statistics.ratio_failed * 100, _statistics.count_skipped)
					_tracer = _tracer.fork ()
				
				for _identifier, _statistics in sorted (_statistics._aggregated.iteritems ()) :
					if _statistics.count_total > 0 :
						_report_statistics (_statistics, _tracer.fork (False))
			
			_report_statistics (self._statistics, _tracer_meta.fork (), True)
			_tracer_meta.cut ()
			
			
			for _task in self._tasks :
				_succeeded = _task._transaction.succeeded
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
				_tracer_meta (0x2d836357, "identifier: `%s`;", _task._identifier)
				_tracer_meta (0xdb41b7d9, "handle: `%s`;", _task._handle)
				_tracer_meta (0xf802fd92, "enforcer: `%s`;", _task._enforcer_handle)
				_tracer_meta.indent (-1)
				_task._transaction._trace (_tracer_meta, True)
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
		
		self.count_planned = 0
		self.count_skipped = 0
		self.count_total = 0
		
		self.ratio_executed = 0
		self.ratio_succeeded = 0
		self.ratio_failed = 0
	
	
	def _update_executed (self, _transaction) :
		
		self.count_executed += 1
		
		if _transaction.succeeded :
			self.count_succeeded += 1
		else :
			self.count_failed += 1
			self.succeeded = False
		
		self.ratio_executed = float (self.count_executed) / self.count_planned
		self.ratio_succeeded = float (self.count_succeeded) / self.count_executed
		self.ratio_failed = float (self.count_failed) / self.count_executed
	
	
	def _update_planned (self) :
		
		self.count_planned += 1
		self.count_total += 1
	
	
	def _update_skipped (self) :
		
		self.count_skipped += 1
		self.count_total += 1




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

