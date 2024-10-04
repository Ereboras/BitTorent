from pieces.torrent import Torrent
import unittest
import datetime

class TestTorrentMethods(unittest.TestCase):

	def test_import_from_ubuntu_file(self):
		torrent = Torrent('torrent-files/ubuntu-24.04.1-desktop-amd64.iso.torrent')
		self.assertEqual(torrent.properties['announce'], 'https://torrent.ubuntu.com/announce')
		self.assertEqual(torrent.properties['created-by'], 'mktorrent 1.1')
		self.assertEqual(torrent.properties['creation-date'], datetime.datetime.fromtimestamp(1724947415))
		self.assertEqual(torrent.properties['name'], 'ubuntu-24.04.1-desktop-amd64.iso')
		self.assertEqual(torrent.properties['info-hash'], '4a3f5e08bcef825718eda30637230585e3330599')
		self.assertEqual(torrent.files, list())

	def test_import_from_debian_file(self):
		torrent = Torrent('torrent-files/debian-12.7.0-amd64-netinst.iso.torrent')
		self.assertEqual(torrent.properties['announce'], 'http://bttracker.debian.org:6969/announce')
		self.assertEqual(torrent.properties['created-by'], 'mktorrent 1.1')
		self.assertEqual(torrent.properties['creation-date'], datetime.datetime.fromtimestamp(1725105953))
		self.assertEqual(torrent.properties['name'], 'debian-12.7.0-amd64-netinst.iso')
		self.assertEqual(torrent.properties['info-hash'], '1bd088ee9166a062cf4af09cf99720fa6e1a3133')
		self.assertEqual(torrent.files, list())

	def test_import_error_filepath_type(self):
		self.assertRaises(TypeError, Torrent, 123)
		self.assertRaises(TypeError, Torrent, tuple)
		self.assertRaises(TypeError, Torrent, dict)

	def test_import_error_wrong_filepath(self):
		self.assertRaises(FileNotFoundError, Torrent, 'torrent-files/fake-file.torrent')

	def test_display_bytes_size_format(self):
		self.assertEqual(Torrent._convertBytes(1000), '1000 bytes')