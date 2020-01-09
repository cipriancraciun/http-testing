



def enforce_identifier (_identifier) :
	if isinstance (_identifier, basestring) :
		pass
	elif isinstance (_identifier, int) :
		pass
	elif isinstance (_identifier, tuple) :
		if len (_identifier) == 0 :
			raise Exception (0x5be9d3f8)
		else :
			_identifier = tuple ([enforce_identifier (_identifier) for _identifier in _identifier])
	else :
		raise Exception (0x17ef4607)
	return _identifier


def stringify_identifier (_identifier) :
	if isinstance (_identifier, basestring) :
		pass
	elif isinstance (_identifier, int) :
		_identifier = str (_identifier)
	elif isinstance (_identifier, tuple) :
		_identifier = [stringify_identifier (_identifier) for _identifier in _identifier if _identifier is not None and _identifier != ()]
		_identifier = " -- ".join (_identifier)
	else :
		raise Exception (0x38729982)
	return _identifier




def normalize_string (_value) :
	
	if _value is None :
		pass
	elif isinstance (_value, basestring) :
		pass
	else :
		raise Exception (0x6d200d15)
	
	if _value == "" :
		_value = None
	
	return _value


def normalize_string_upper (_value) :
	_value = normalize_string (_value)
	if _value is not None :
		_value = _value.upper ()
	return _value

def normalize_string_lower (_value) :
	_value = normalize_string (_value)
	if _value is not None :
		_value = _value.lower ()
	return _value




def normalize_positive_integer (_value) :
	
	if _value is None :
		pass
	elif isinstance (_value, int) :
		if _value <= 0 :
			raise Exception (0x5e536bf2)
	else :
		raise Exception (0x4904782e)
	
	return _value




def enforce_string (_value) :
	return enforce_type (_value, basestring, False)

def enforce_string_or_none (_value) :
	return enforce_type (_value, basestring, True)


def enforce_type (_value, _type, _allow_none) :
	
	if _value is None :
		if not _allow_none :
			raise Exception (0x5b0e4a45)
	elif not isinstance (_value, _type) :
		raise Exception (0x11a4ebf9)
	
	return _value




def flatten_list (_value, _normalizer = None, _enforcer = None) :
	_accumulator = []
	flatten_list_0 (_accumulator, _value, False, False, False, _normalizer, _enforcer)
	return _accumulator

def flatten_list_or_similar (_value, _normalizer = None, _enforcer = None) :
	_accumulator = []
	flatten_list_0 (_accumulator, _value, True, True, True, _normalizer, _enforcer)
	return _accumulator


def flatten_list_0 (_accumulator, _value, _flatten_none, _flatten_tuples, _flatten_sets, _normalizer, _enforcer) :
	
	if isinstance (_value, list) :
		pass
		
	elif isinstance (_value, tuple) :
		if not _flatten_tuples :
			_accumulator.append (_value)
			return
		
	elif isinstance (_value, set) :
		if not _flatten_sets :
			_accumulator.append (_value)
			return
		
	else :
		
		if _normalizer is not None :
			_value = _normalizer (_value)
		
		if _value is None :
			if _flatten_none :
				return
		
		if _enforcer is not None :
			_enforcer (_value)
		
		_accumulator.append (_value)
		return
	
	for _value in _value :
		flatten_list_0 (_accumulator, _value, _flatten_none, _flatten_tuples, _flatten_sets, _normalizer, _enforcer)




def flatten_multi_map (_value, _key_normalizer = None, _key_enforcer = None, _value_normalizer = None, _value_enforcer = None) :
	_accumulator = []
	flatten_multi_map_0 (_accumulator, _value, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer)
	return _accumulator


def flatten_multi_map_0 (_accumulator, _value, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer) :
	
	if _value is None :
		return
		
	elif isinstance (_value, tuple) :
		if len (_value) < 1 :
			raise Exception (0xf7b6e4b4)
		_key = _value[0]
		_value = _value[1:]
		flatten_multi_map_0_pair (_accumulator, _key, _value, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer)
		
	elif isinstance (_value, list) or isinstance (_value, set) :
		for _value in _value :
			flatten_multi_map_0 (_accumulator, _value, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer)
		
	elif isinstance (_value, dict) :
		for _key, _value in _value.iteritems () :
			flatten_multi_map_0_pair (_accumulator, _key, _value, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer)
	
	else :
		raise Exception (0xc540f5c1)


def flatten_multi_map_0_pair (_accumulator, _key, _value, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer) :
	
	if _key_normalizer is not None :
		_key = _key_normalizer (_key)
	
	if _key_enforcer is not None :
		_key_enforcer (_key)
	
	def _recurse (_value) :
		
		if _value is None :
			return
			
		elif isinstance (_value, tuple) or isinstance (_value, list) or isinstance (_value, set) :
			for _value in _value :
				_recurse (_value)
			
		else :
			
			if _value_normalizer is not None :
				_value = _value_normalizer (_value)
			
			if _value is None :
				return
			
			if _value_enforcer is not None :
				_value_enforcer (_value)
			
			_accumulator.append ((_key, _value))
	
	_recurse (_value)




def multi_map_to_dict (_map, _key_normalizer = None, _key_enforcer = None, _value_normalizer = None, _value_enforcer = None) :
	_accumulator = {}
	multi_map_to_dict_0 (_accumulator, _map, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer)
	return _accumulator


def multi_map_to_dict_0 (_accumulator, _map, _key_normalizer, _key_enforcer, _value_normalizer, _value_enforcer) :
	
	if _map is None :
		return
	
	for _key, _value in _map :
		
		if _key_normalizer is not None :
			_key = _key_normalizer (_key)
		if _key is None :
			continue
		if _key_enforcer is not None :
			_key_enforcer (_key)
		
		if _value_normalizer is not None :
			_value = _value_normalizer (_value)
		if _value is None :
			continue
		if _value_enforcer is not None :
			_value_enforcer (_value)
		
		if _key not in _accumulator :
			if isinstance (_value, list) :
				_value = list (_value)
			_accumulator[_key] = _value
		else :
			_values = _accumulator[_key]
			if not isinstance (_values, list) :
				_values = [_values]
				_accumulator[_key] = _values
			_values.append (_value)

