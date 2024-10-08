from collections import OrderedDict

class Encoder:

	encoding: str = 'utf-8'

	def __init__(self, data):
		if not self._isDataTypeValid(data):
			raise TypeError(f'Bencode data must be of type str, int, list or OrderedDict, not {type(data)}')
		self.data = data

	def encode(self) -> bytearray:
		return self._encodeDispatcher(self.data)
	
	def _encodeDispatcher(self, data) -> bytearray:
		tmpLine: bytearray = bytearray()
		if isinstance(data, int):
			tmpLine = self._encodeInt(data)
		elif isinstance(data, str):
			tmpLine = self._encodeStr(data)
		elif isinstance(data, bytes):
			tmpLine = self._encodeBytes(data)
		elif isinstance(data, list):
			tmpLine = self._encodeList(data)
		else:
			tmpLine = self._encodeOrderedDict(data)

		return tmpLine
	
	def _encodeInt(self, data: int) -> bytearray:
		return ('i' + str(data) + 'e').encode(self.encoding)
	
	def _encodeStr(self, data: str) -> bytearray:
		return (str(len(data)) + ':' + data).encode(self.encoding)
	
	def _encodeBytes(self, data: bytes) -> bytearray:
		return (str(len(data))).encode(self.encoding) + b':' + data
	
	def _encodeList(self, data: list) -> bytearray:
		tmpLine: bytearray = b'l'

		for value in data:
			if not self._isDataTypeValid(value):
				raise TypeError(f'Value in list must be of type str, int, list or OrderedDict, not {type(value)}')
			tmpLine += self._encodeDispatcher(value)

		tmpLine += b'e'
		return tmpLine
	
	def _encodeOrderedDict(self, data: OrderedDict) -> bytearray:
		tmpLine: bytearray = b'd'
		for key, value in data.items():
			if not isinstance(key, str) and not isinstance(key, bytes):
				raise TypeError(f'Key in OrderedDict must be of type str or bytes for bencode encoding, not {type(key)}')
			if not self._isDataTypeValid(value):
				raise TypeError(f'Value in OrderedDict must be of type str, int, list or OrderedDict, not {type(value)}')
			
			tmpLine += self._encodeDispatcher(key) + self._encodeDispatcher(value)

		tmpLine += b'e'
		return tmpLine
	
	def _isDataTypeValid(self, data) -> bool:
		return isinstance(data, int) or isinstance(data, str) or isinstance(data, list) or isinstance(data, OrderedDict) or isinstance(data, bytes)
	
class Decoder:

	def __init__(self, data: bytes):
		self.data = data
		self.index = 0

	def decode(self):
		if self.index > len(self.data):
			return None
		nextChar = self.data[self.index:self.index + 1] # Python automatically cast to int if accessed directly with self.index, so we use slicing instead

		if nextChar is None or nextChar == b'':
			raise EOFError('Unexpected end of data, there might be a missing end marker in the data provided')
		
		if nextChar == b'i':
			self.index += 1
			return self._decodeInt()
		elif nextChar in b'0123456789':
			return self._decodeStr() 
		elif nextChar == b'l':
			self.index += 1
			return self._decodeList()
		elif nextChar == b'd':
			self.index += 1
			return self._decodeDict()

	def _readUntil(self, token: bytes) -> bytes:
		try:
			indexEnd = self.data.index(token, self.index)
			data = self.data[self.index:indexEnd]
			self.index = indexEnd + 1
			return data
		except:
			raise EOFError(f'Unable to find token {str(token)}')

	def _decodeInt(self) -> int:
		return int(self._readUntil(b'e'))
	
	def _decodeStr(self) -> bytes:
		lengthStr = int(self._readUntil(b':'))
		if self.index + lengthStr > len(self.data):
			raise EOFError(f'Unexpected end of data, string at position {self.index} specify {lengthStr} chars long but data is only {len(self.data)} bytes')
		tmpStr = self.data[self.index:self.index + lengthStr]
		self.index += lengthStr
		return tmpStr
	
	def _decodeList(self) -> list:
		tmpList = []
		while self.data[self.index:self.index + 1] != b'e':
			tmpList.append(self.decode())
		self.index += 1
		return tmpList
	
	def _decodeDict(self) -> OrderedDict:
		tmpDict = OrderedDict()
		while self.data[self.index:self.index + 1] != b'e':
			key = self.decode()
			if not isinstance(key, bytes):
				raise TypeError(f'Key {key} is of type {type(key)} but key of Ordered dict must be of string format')
			value = self.decode()
			tmpDict[key] = value
		self.index += 1
		return tmpDict