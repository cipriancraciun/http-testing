

import random




# NOTE:  https://github.com/volution/vonuvoli-scheme/blob/development/sources/counters.rs


class Permuter (object) :
	
	def __init__ (self, _seed_1 = None, _seed_2 = None) :
		if _seed_1 is None :
			_seed_1 = _permutation_random.getrandbits (32)
		if _seed_2 is None :
			_seed_2 = _permutation_random.getrandbits (32)
		self._count = 0
		self._index = _permutation_permute (_permutation_permute (_seed_1) + _permutation_fuzz_2)
		self._offset = _permutation_permute (_permutation_permute (_seed_2) + _permutation_fuzz_3)
	
	
	def next (self) :
		self._count += 1
		self._index += 1
		_output = self._index
		_output = _permutation_permute (_output)
		_output = _output + self._offset
		_output = _permutation_permute (_output)
		_output = _output ^ _permutation_fuzz_1
		return _output


def _permutation_permute (_index) :
	_index = _index & 0xffffffff
	if _index >= _permutation_prime :
		return _index
	_index_2 = (_index * _index) & 0xffffffffffffffff
	_residue = _index_2 % _permutation_prime
	if _index <= (_permutation_prime / 2) :
		return _residue
	else :
		return _permutation_prime - _residue


_permutation_random = random.SystemRandom ()
_permutation_prime = 0xfffffffb
_permutation_fuzz_1 = 0x5bf03635
_permutation_fuzz_2 = 0x682f0161
_permutation_fuzz_3 = 0x46790905

