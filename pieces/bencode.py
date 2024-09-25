from collections import OrderedDict

class Encoder:

	def __init__(self, data):
		if not self._isDataTypeValid(data):
			raise TypeError(f'Bencode data must be of type str, int, list or OrderedDict, not {type(data)}')
		self.data = data

	def encode(self) -> bytes:
		return self._encodeDispatcher(self.data).encode('utf-8')
	
	def _encodeDispatcher(self, data) -> str:
		tmpLine = ''
		if isinstance(data, int):
			tmpLine = self._encodeInt(data)
		elif isinstance(data, str):
			tmpLine = self._encodeStr(data)
		elif isinstance(data, list):
			tmpLine = self._encodeList(data)
		else:
			tmpLine = self._encodeOrderedDict(data)

		return tmpLine
	
	def _encodeInt(self, data: int) -> str:
		tmpLine = 'i'
		tmpLine += str(data)
		tmpLine += 'e'
		return tmpLine
	
	def _encodeStr(self, data: str) -> str:
		tmpLine = str(len(data))
		tmpLine += ':'
		tmpLine += data

		return tmpLine
	
	def _encodeList(self, data: list) -> str:
		tmpLine = 'l'

		for value in data:
			if not self._isDataTypeValid(value):
				raise TypeError(f'Value in list must be of type str, int, list or OrderedDict, not {type(value)}')
			tmpLine += self._encodeDispatcher(value)

		tmpLine += 'e'
		return tmpLine
	
	def _encodeOrderedDict(self, data: OrderedDict) -> str:
		tmpLine = 'd'
		for key, value in data.items():
			if not isinstance(key, str):
				raise TypeError(f'Key in OrderedDict must be of type str for bencode encoding, not {type(key)}')
			if not self._isDataTypeValid(value):
				raise TypeError(f'Value in OrderedDict must be of type str, int, list or OrderedDict, not {type(value)}')
			
			tmpLine += self._encodeDispatcher(key) + self._encodeDispatcher(value)

		tmpLine += 'e'
		return tmpLine
	
	def _isDataTypeValid(self, data) -> bool:
		return isinstance(data, int) or isinstance(data, str) or isinstance(data, list) or isinstance(data, OrderedDict)