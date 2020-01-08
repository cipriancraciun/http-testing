
import logging
import thread, threading


logging.NOTICE = (logging.INFO + logging.WARNING) / 2
logging.addLevelName (logging.NOTICE, "NOTICE")

logging.CUT = logging.INFO + 1
logging.addLevelName (logging.CUT, "----")

logging.INTERNAL = (logging.NOTSET + logging.DEBUG) / 2
logging.addLevelName (logging.INTERNAL, "DEBUG")

logging.DUMP = logging.CRITICAL * 2
logging.addLevelName (logging.DUMP, "DUMP")


_logging_level = logging.NOTICE
_logging_level = logging.INFO
# _logging_level = logging.DEBUG
# _logging_level = logging.NOTSET + 1


if len (logging.root.handlers) == 0 :
	
	try :
		import colorlog
	except :
		colorlog = None
	
	if colorlog is not None :
		_logging_handler = colorlog.StreamHandler ()
		_logging_handler.setFormatter (colorlog.ColoredFormatter (
				"%(log_color)s[%(levelname)-4.4s] %(message)s",
				datefmt = "%Y-%m-%d %H:%M:%S",
				reset = True,
				log_colors = {
						"CRITICAL" : "bold_red",
						"ERROR" : "red",
						"WARNING" : "yellow",
						"NOTICE" : "green",
						"----" : "cyan",
						"INFO" : "white",
						"DEBUG" : "white",
						"DUMP" : "purple",
				}
			))
		
	else :
		_logging_handler = logging.StreamHandler ()
		_logging_handler.setFormatter (logging.Formatter ("[%(levelname)-4.4s] %(message)s", "%Y-%m-%d %H:%M:%S"))
	
	logging.root.addHandler (_logging_handler)
	logging.root.setLevel (_logging_level)




from counters import *




class Tracer (object) :
	
	
	def __init__ (self) :
		self._indent = 0
	
	
	def critical (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.CRITICAL, _code, _arguments_list, _arguments_dict, None)
	
	def error (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.ERROR, _code, _arguments_list, _arguments_dict, None)
	
	def warning (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.WARNING, _code, _arguments_list, _arguments_dict, None)
	
	def notice (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.NOTICE, _code, _arguments_list, _arguments_dict, None)
	
	def info (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.INFO, _code, _arguments_list, _arguments_dict, None)
	
	def debug (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.DEBUG, _code, _arguments_list, _arguments_dict, None)
	
	def internal (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.INTERNAL, _code, _arguments_list, _arguments_dict, None)
	
	def _push (self, _level, _code, _arguments_list, _arguments_dict, _indent) :
		return self._log (_level, _code, _arguments_list, _arguments_dict, _indent)
	
	
	def critical_tracer (self, _indent = False) :
		return TracerFunc (self, self._push, logging.CRITICAL, _indent)
	
	def error_tracer (self, _indent = False) :
		return TracerFunc (self, self._push, logging.ERROR, _indent)
	
	def warning_tracer (self, _indent = False) :
		return TracerFunc (self, self._push, logging.WARNING, _indent)
	
	def notice_tracer (self, _indent = False) :
		return TracerFunc (self, self._push, logging.NOTICE, _indent)
	
	def info_tracer (self, _indent = False) :
		return TracerFunc (self, self._push, logging.INFO, _indent)
	
	def debug_tracer (self, _indent = False) :
		return TracerFunc (self, self._push, logging.DEBUG, _indent)
	
	def internal_tracer (self, _indent = False) :
		return TracerFunc (self, self._push, logging.INTERNAL, _indent)
	
	
	def fork (self, _indent = True) :
		_fork = self._fork ()
		_fork._indent = _merge_indent (self._indent, _indent)
		return _fork
	
	def _fork (self) :
		raise Exception (0x24b5c482)




class TracerFunc (object) :
	
	
	def __init__ (self, _tracer, _push, _level, _indent) :
		
		self._tracer = _tracer
		self._push = _push
		self._level = _level
		
		self._indent = _merge_indent (None, _indent)
	
	
	def __call__ (self, _code, *_arguments_list, **_arguments_dict) :
		self._push (self._level, _code, _arguments_list, _arguments_dict, self._indent)
	
	
	def fork (self, _indent = True) :
		_indent = _merge_indent (self._indent, _indent)
		_fork = TracerFunc (self._tracer, self._push, self._level, _indent)
		return _fork
	
	
	def cut (self) :
		self._tracer.cut ()
	
	def indent (self, _indent = True) :
		self._indent = _merge_indent (self._indent, _indent)




class Transcript (Tracer) :
	
	
	def __init__ (self, _owner, _code, _instance = None) :
		Tracer.__init__ (self)
		
		self._code = _code
		self._instance = _instance
		
		if isinstance (_owner, logging.Logger) :
			self._logger = _owner
		elif isinstance (_owner, basestring) :
			self._logger = logging.getLogger (_owner)
		else :
			raise Exception (0x46e8f4e5)
	
	
	def _fork (self) :
		_fork = Transcript (self._logger, self._code, self._instance)
		return _fork
	
	
	def cut (self) :
		global _transcript_last_was_cut
		with _transcript_mutex :
			if _transcript_last_was_cut :
				return
			self._logger.log (logging.CUT, "----------------------------")
			_transcript_last_was_cut = True
	
	
	def _log (self, _level, _code, _arguments_list, _arguments_dict, _indent) :
		global _transcript_last_was_cut
		if self._logger.isEnabledFor (_level) :
			_message = _arguments_list[0]
			_arguments_list = _arguments_list[1:]
			_indent = _merge_indent (self._indent, _indent)
			_thread_ident = thread.get_ident ()
			if _thread_ident == _transcript_main_thread_ident :
				_prefix = "[%08x:%08x:%08x]    " % (self._code, self._instance, _code)
			else :
				_prefix = "[%016x][%08x:%08x:%08x]    " % (_thread_ident, self._code, self._instance, _code)
			_prefix += "|  " * _indent
			with _transcript_mutex :
				self._logger._log (_level, _prefix + _message, tuple (_arguments_list), **_arguments_dict)
				_transcript_last_was_cut = False


_transcript_last_was_cut = False
_transcript_main_thread_ident = thread.get_ident ()
_transcript_mutex = threading.Lock ()




class Dumper (Tracer) :
	
	
	def __init__ (self, _target = None) :
		Tracer.__init__ (self)
		
		if _target is None :
			self._logger = _dumper_logger
			
		elif isinstance (_target, logging.Logger) :
			self._logger = _target
			
		elif isinstance (_target, logging.Handler) :
			_logger = logging.Logger ("{dump}", logging.NOTSET + 1)
			_logger.addHandler (_target)
			_logger.propagate = False
			self._logger = _logger
			
		elif isinstance (_target, file) :
			_handler = logging.StreamHandler (_target)
			_handler.setFormatter (logging.Formatter ("%(message)s", "%Y-%m-%d %H:%M:%S"))
			_logger = logging.Logger ("{dump}", logging.NOTSET + 1)
			_logger.addHandler (_handler)
			_logger.propagate = False
			self._logger = _logger
			
		elif isinstance (_target, basestring) :
			self._logger = logging.getLogger (_target)
			
		else :
			raise Exception (0xd3ba4028)
		
		self._last_was_cut = False
	
	
	def _fork (self) :
		_fork = Dumper ()
		return _fork
	
	
	def cut (self) :
		if self._last_was_cut :
			return
		self._logger.log (logging.CUT, "")
		self._logger.log (logging.CUT, "            ------------------------------------------------------------")
		self._logger.log (logging.CUT, "")
		self._last_was_cut = True
	
	
	def _log (self, _level, _code, _arguments_list, _arguments_dict, _indent) :
		_message = _arguments_list[0]
		_arguments_list = _arguments_list[1:]
		_indent = _merge_indent (self._indent, _indent)
		_prefix = "[%08x]  " % (_code)
		_prefix += "    " * _indent
		self._logger.log (_level, _prefix + _message, *_arguments_list, **_arguments_dict)
		self._last_was_cut = False




class Annotations (Tracer) :
	
	
	def __init__ (self) :
		Tracer.__init__ (self)
		self._logger = logging.Logger ("{annotations}")
		self._logger.handle = lambda _record : self._records.append (_record)
		self._records = list ()
	
	
	def _log (self, _level, _code, _arguments_list, _arguments_dict, _indent) :
		_message = _arguments_list[0]
		_arguments_list = _arguments_list[1:]
		_indent = _merge_indent (self._indent, _indent)
		_prefix = "[%08x]  " % _code
		self._logger.log (_level, _prefix + _message, *_arguments_list, **_arguments_dict)
	
	def _propagate (self, _tracer) :
		_arguments_dict = {}
		for _record in self._records :
			_arguments_list = [_record.msg]
			_arguments_list.extend (_record.args)
			_tracer._push (_record.levelno, 0xd06d66d4, _arguments_list, _arguments_dict, self._indent)




def _merge_indent (_base, _offset) :
	
	if _base is None :
		_base = 0
	elif isinstance (_base, int) :
		pass
	else :
		raise Exception (0x726e6666)
	
	if _offset is True :
		_offset = 1
	elif _offset is False or _offset is None :
		_offset = 0
	elif isinstance (_offset, int) :
		pass
	else :
		raise Exception (0x26036305)
	
	return _base + _offset




def transcript (_owner, _code, _instance = None) :
	
	if _instance is None :
		_instance = _transcript_instance_permuter.next ()
	
	if isinstance (_owner, basestring ):
		pass
	elif isinstance (_owner, type) :
		_owner = "%s.%s" % (_owner.__module__, _owner.__name__)
	elif isinstance (_owner, object) :
		_owner = type (_owner)
		_owner = "%s.%s" % (_owner.__module__, _owner.__name__)
	else :
		raise Exception (0xe1952180)
	
	return Transcript (_owner, _code, _instance)


_transcript_instance_permuter = Permuter ()




def dumper (_stream) :
	if isinstance (_stream, Dumper) :
		return TracerFunc (_stream, _stream._push, logging.DUMP, None)
	elif isinstance (_stream, TracerFunc) :
		return _dumper
	else :
		return dumper (Dumper (_stream))


_dumper_logger_handler = logging.StreamHandler ()
_dumper_logger_handler.setFormatter (logging.Formatter ("%(message)s", "%Y-%m-%d %H:%M:%S"))

_dumper_logger = logging.Logger ("{dump}", logging.NOTSET + 1)
_dumper_logger.addHandler (_dumper_logger_handler)
_dumper_logger.propagate = False


dump = dumper (None)

