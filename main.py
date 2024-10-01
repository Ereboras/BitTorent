from pieces.torrent import Torrent
import argparse

def main():
	parser = argparse.ArgumentParser(
		description='This BitTorrent client can be used to download file through BitTorrent protocol.',
	)

	parser.add_argument('filepath',help='The path to the torrent file')
	args = parser.parse_args()

	print(Torrent(args.filepath))

if __name__ == '__main__':
	main()