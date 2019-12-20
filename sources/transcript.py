

import logging




_transcript_trace = False

logging.basicConfig (
		# NOTE:  https://docs.python.org/2/library/logging.html#logrecord-attributes
		# format = "[%(process)08d][%(levelname)-8s}][%(name)-25s]  %(message)s",
		format = "%(levelname)8s %(message)s",
		datefmt = "%Y-%m-%d %H:%M:%S",
		level = logging.INFO if not _transcript_trace else 0,
	)

logging.addLevelName (logging.DEBUG / 2, "TRACE")




from counters import *




class Tracer (object) :
	
	
	def critical (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.CRITICAL, _code, _arguments_list, _arguments_dict)
	
	def error (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.ERROR, _code, _arguments_list, _arguments_dict)
	
	def warning (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.WARNING, _code, _arguments_list, _arguments_dict)
	
	def info (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.INFO, _code, _arguments_list, _arguments_dict)
	
	def debug (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.DEBUG, _code, _arguments_list, _arguments_dict)
	
	def trace (self, _code, *_arguments_list, **_arguments_dict) :
		return self._log (logging.DEBUG / 2, _code, _arguments_list, _arguments_dict)




class Transcript (Tracer) :
	
	
	def __init__ (self, _owner, _code, _instance = None) :
		self._logger = logging.getLogger (_owner)
		self._code = _code
		self._instance = _instance
	
	
	def _log (self, _level, _code, _arguments_list, _arguments_dict) :
		_message = _arguments_list[0]
		_arguments_list = _arguments_list[1:]
		_prefix = "[%08x:%08x:%08x]  " % (self._code, self._instance, _code)
		self._logger.log (_level, _prefix + _message, *_arguments_list, **_arguments_dict)




class Annotations (Tracer) :
	
	
	def __init__ (self) :
		self._logger = logging.Logger ("{annotations}")
		self._logger.handle = lambda _record : self._records.append (_record)
		self._records = list ()
	
	
	def _log (self, _level, _code, _arguments_list, _arguments_dict) :
		_message = _arguments_list[0]
		_arguments_list = _arguments_list[1:]
		_prefix = "[%08x]  " % _code
		self._logger.log (_level, _prefix + _message, *_arguments_list, **_arguments_dict)




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

