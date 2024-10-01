from pieces.torrent import Torrent
from pieces.bencode import Decoder
from urllib.parse import urlencode
import random
import aiohttp
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
			'peer_id': self._generatePeerId(),
			'uploaded': uploaded,
			'downloaded': downloaded,
			'left': self._calculateSizeLeftToDownload(),
			'port': port,
			'compact': int(compact)
		}

		urlParams: str = self.torrent.properties['announce'] + '?' + urlencode(dictUrlParams)

		async with aiohttp.ClientSession() as session:
			async with session.get(urlParams) as response:
				if not response.status == 200:
					raise ConnectionError('Unable to connect to tracker')

				bodyResponse = await response.text()
				self.trackerData = Decoder(bodyResponse.encode('utf-8')).decode()

	def _generatePeerId(self) -> str:
		return '-' + 'UT' + '0001' + '-' + ''.join([str(random.randint(0,9)) for _ in range(12)])
	
	def _calculateSizeLeftToDownload(self) -> int:
		totalSize: int = 0
		for file in self.torrent.files:
			totalSize += file['length']
		return totalSize