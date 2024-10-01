from pieces.bencode import Decoder
from collections import OrderedDict
import datetime

class Torrent:

	def __init__(self, filePath: str):
		if not isinstance(filePath, str):
			raise TypeError(f'File path must be str, filePath is {type(data)} instead')
		
		with open(filePath, 'rb') as f:
			meta_info = f.read()
			fileData = Decoder(meta_info).decode()

		self._importProperties(fileData)
		self._importFiles(fileData)

	def _importProperties(self, data : OrderedDict):
		self.properties = dict()

		if b'encoding' in data:
			self.properties['encoding'] = data[b'encoding'].decode('ascii')
		else:
			self.properties['encoding'] = 'ascii'

		if b'announce' in data:
			self.properties['announce'] = data[b'announce'].decode(self.properties['encoding'])
		if b'created by' in data:
			self.properties['created-by'] = data[b'created by'].decode(self.properties['encoding'])
		if b'creation date' in data:
			self.properties['creation-date'] = datetime.datetime.fromtimestamp(data[b'creation date'])
		if b'info' in data and b'name' in data[b'info']:
			self.properties['name'] = data[b'info'][b'name'].decode(self.properties['encoding'])
		if b'info' in data and b'length' in data[b'info']:
			self.properties['length'] = data[b'info'][b'length'].decode(self.properties['encoding'])
		if b'info' in data and b'piece length' in data[b'info']:
			self.properties['piece-length'] = self._convertBytes(data[b'info'][b'piece length'])

	def _importFiles(self, data : OrderedDict):
		self.files = list()

		if b'info' in data and b'files' in data[b'info']:
			for file in data[b'info'][b'files']:
				tmpDict = dict()
				if b'path' in file:
					tmpDict['path'] = file[b'path'][0].decode(self.properties['encoding'])
					tmpDict['length'] = file[b'length']
					self.files.append(tmpDict)

	def _formatProperties(self, key, displayKey):
		tmpStr = ''
		if key in self.properties:
			tmpStr += f'{displayKey: <16}: {self.properties[key]}\n'
		return tmpStr
	
	def _formatFiles(self):
		tmpStr = ''

		for file in self.files:
			tmpStr += f'{'Path': <16}: {file['path']}\n'
			tmpStr += f'{'Length': <16}: {self._convertBytes(file['length'])}\n'
			tmpStr += '|============================|\n'
		return tmpStr

	def _convertBytes(self, size):
		for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
			if size < 1024.0:
				return "%3.1f %s" % (size, x)
			size /= 1024.0

		return size

	def __str__(self):
		tmpStr = '|============================|\n'
		tmpStr += '|=========| TORRENT |========|\n'
		tmpStr += '|============================|\n'

		tmpStr += self._formatProperties('announce', 'Announce')
		tmpStr += self._formatProperties('created-by', 'Created by')
		tmpStr += self._formatProperties('encoding', 'Encoding')
		tmpStr += self._formatProperties('creation-date', 'Creation date')
		tmpStr += self._formatProperties('name', 'Name')
		tmpStr += self._formatProperties('length', 'Length')
		tmpStr += self._formatProperties('piece-length', 'Piece length')

		tmpStr += '|=========== FILES ==========|\n'
		tmpStr += self._formatFiles()
		return tmpStr