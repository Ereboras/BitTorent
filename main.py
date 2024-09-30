from collections import OrderedDict
from pieces.bencode import Encoder, Decoder
from pieces.torrent import Torrent

with open('torrent-files/example.torrent', 'rb') as f:
	meta_info = f.read()
	torrent = Decoder(meta_info).decode()

print(Torrent(torrent))