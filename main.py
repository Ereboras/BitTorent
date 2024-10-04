from pieces.torrent import Torrent
from pieces.tracker import Tracker
import argparse
import asyncio
import logging


def main():
	parser = argparse.ArgumentParser(
		description='This BitTorrent client can be used to download file through BitTorrent protocol.',
	)

	parser.add_argument('filepath',help='The path to the torrent file')
	parser.add_argument('-v', '--verbose', action='store_true')

	args = parser.parse_args()

	logLevel = logging.INFO
	if args.verbose:
		logLevel = logging.DEBUG

	logging.basicConfig(
		level=logLevel,
		format="%(asctime)s [%(levelname)s] %(message)s",
		handlers=[
			logging.FileHandler("logs/debug.log"),
			logging.StreamHandler()
		]
	)

	torrent = Torrent(args.filepath)
	print(torrent)
	tracker = Tracker(torrent)
	asyncio.run(tracker.connect())
	print(tracker)

if __name__ == '__main__':
	main()