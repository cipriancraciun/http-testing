

import md5




def fingerprint (_value) :
	_hasher = md5.new ()
	_fingerprint_0 (_hasher, _value)
	_hash = _hasher.digest ()
	_hash = _hash.encode ("hex")
	return _hash


def _fingerprint_0 (_hasher, _value) :
	
	if _value is None :
		_hasher.update ("none")
		
	elif _value is True :
		_hasher.update ("true")
		
	elif _value is False :
		_hasher.update ("false")
		
	elif isinstance (_value, basestring) :
		_hasher.update (_value)
		
	elif isinstance (_value, int) or isinstance (_value, float) :
		_hasher.update (str (_value))
		
	elif isinstance (_value, tuple) or isinstance (_value, list) or isinstance (_value, set) :
		
		if isinstance (_value, tuple) :
			_hasher.update ("tuple")
		elif isinstance (_value, list) :
			_hasher.update ("list")
		elif isinstance (_value, set) :
			_hasher.update ("set")
			_value = sorted (_value)
		else :
			raise Exception (0xfc11cc66)
		
		_hasher.update (str (len (_value)))
		
		for _value in _value :
			_fingerprint_0 (_hasher, _value)
		
	elif isinstance (_value, dict) :
		
		_hasher.update ("dict")
		_hasher.update (str (len (_value)))
		
		for _key, _value in sorted (_value.iteritems ()) :
			_fingerprint_0 (_hasher, _key)
			_fingerprint_0 (_hasher, _value)
		
	else :
		raise Exception ((0x7f3881aa, _value))




def hash_md5 (_value) :
	_hasher = md5.new ()
	_hash_0 (_hasher, _value)
	_hash = _hasher.digest ()
	_hash = _hash.encode ("hex")
	return _hash


def _hash_0 (_hasher, _value) :
	
	if _value is None :
		pass
		
	elif isinstance (_value, basestring) :
		_hasher.update (_value)
		
	elif isinstance (_value, tuple) or isinstance (_value, list) :
		
		for _value in _value :
			_hash_0 (_hasher, _value)
		
	else :
		raise Exception ((0x23a8d044, _value))

