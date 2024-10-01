from pieces.torrent import Torrent
from pieces.tracker import Tracker
import argparse
import asyncio


def main():
	parser = argparse.ArgumentParser(
		description='This BitTorrent client can be used to download file through BitTorrent protocol.',
	)

	parser.add_argument('filepath',help='The path to the torrent file')
	args = parser.parse_args()

	torrent = Torrent(args.filepath)
	tracker = Tracker(torrent)
	asyncio.run(tracker.connect())

if __name__ == '__main__':
	main()