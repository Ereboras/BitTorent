from pieces.torrent import Torrent
from pieces.bencode import Decoder, Encoder
from urllib.parse import urlencode
import random
import aiohttp
import hashlib
import pathlib
import os
import time
import logging
from collections import OrderedDict

class Tracker:

	def __init__(self, torrent: Torrent):
		if not isinstance(torrent, Torrent):
			raise TypeError(f'torrent arg must be Torrent type, not {type(torrent)}')
		self.torrent = torrent
		self.trackerData = OrderedDict()
	
	async def connect(self, uploaded : int = 0, downloaded : int = 0, port : int = 6889, compact : bool = True):
		if 'info-hash' not in self.torrent.properties:
			raise RuntimeError('Missing parameters info-hash in torrent properties')
		if 'announce' not in self.torrent.properties:
			raise RuntimeError('Missing parameters announce in torrent properties')
		
		dictUrlParams: dict = {
			'info_hash': self.torrent.properties['info-hash'],
			'uploaded': uploaded,
			'downloaded': downloaded,
			'left': self._calculateSizeLeftToDownload(),
			'port': port,
			'compact': int(compact)
		}

		filenameToOpen = hashlib.sha1(urlencode(dictUrlParams).encode('utf-8'), usedforsecurity=False).hexdigest()
		filePath = pathlib.Path(f'tmp/{filenameToOpen}')
		shouldConnect = False
		if filePath.is_file():
			with filePath.open() as f:
				rawData = f.read().encode('utf-8')
				self.trackerData = Decoder(rawData).decode()

				now = time.time()
				nextTimestamp = self._timeUntilNextRequest(filePath)
				logging.debug(f'File found at {filePath.absolute()}, valid until {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(nextTimestamp))}.')
				if now > nextTimestamp:
					logging.debug(f'File is not valid anymore (current time {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))}), sending request to tracker...')
					shouldConnect = True
		else:
			shouldConnect = True

		if shouldConnect:
			await self._connectToTracker(dictUrlParams, filePath)

	async def _connectToTracker(self, dictUrlParams: dict, filePath: pathlib.Path):
		dictUrlParams['peer_id'] = self._generatePeerId()
		urlParams: str = self.torrent.properties['announce'] + '?' + urlencode(dictUrlParams)
		logging.debug(f'Url generated for tracker : {urlParams}')

		async with aiohttp.ClientSession() as session:
			async with session.get(urlParams) as response:
				bodyResponse = await response.read()
				self.trackerData = Decoder(bodyResponse).decode()

				if 'failure reason' in self.trackerData:
					raise RuntimeError(f'An error was sent by tracker : {self.trackerData[b'failure reason']}')
				if not response.status == 200:
					raise ConnectionError(f'Unable to connect to tracker : code {response.status} was sent back')

				peers = list()
				for i in range(0, len(self.trackerData[b'peers']), 6):
					tmpPeerInfosDict = OrderedDict()
					tmpPeerInfosDict[b'ip'] = bytes('.'.join([str(peerByte) for peerByte in self.trackerData[b'peers'][i:i+4]]), 'utf-8')
					tmpPeerInfosDict[b'port'] = int.from_bytes(self.trackerData[b'peers'][i+4:i+6], byteorder='big')
					peers.append(tmpPeerInfosDict)

				self.trackerData[b'peers'] = peers
				with filePath.open('w') as f:
					f.write(Encoder(self.trackerData).encode().decode('utf-8'))
					logging.debug(f'File generated at {filePath.absolute()}. This file will be valid until {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self._timeUntilNextRequest(filePath)))}')

	def _timeUntilNextRequest(self, filePath: pathlib.Path):
		return os.path.getmtime(filePath) + self.trackerData[b'interval']
	
	def _generatePeerId(self) -> str:
		return '-' + 'PC' + '0001' + '-' + ''.join([str(random.randint(0,9)) for _ in range(12)])
	
	def _calculateSizeLeftToDownload(self) -> int:
		totalSize: int = 0
		for file in self.torrent.files:
			totalSize += file['length']
		return totalSize
	
	def _formatProperties(self, key, displayKey):
		tmpStr = ''
		if key in self.trackerData:
			tmpStr += f'{displayKey: <16}: {self.trackerData[key]}\n'
		return tmpStr
	
	def __str__(self):
		tmpStr = '|============================|\n'
		tmpStr += '|=========| TRACKER |========|\n'
		tmpStr += '|============================|\n'
		tmpStr += self._formatProperties(b'complete', 'Complete')
		tmpStr += self._formatProperties(b'incomplete', 'Incomplete')
		tmpStr += self._formatProperties(b'interval', 'Interval (in seconds)')

		tmpStr += '|=========== PEERS ==========|\n'
		for peer in self.trackerData[b'peers']:
			tmpStr += peer[b'ip'].decode('utf-8') + ':' + str(peer[b'port']) + '\n'
		tmpStr += '|============================|\n'
		return tmpStr