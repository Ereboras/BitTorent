import unittest
from collections import OrderedDict
from pieces.bencode import Encoder, Decoder

class TestBencodeMethods(unittest.TestCase):

    def test_encode_int(self):
        self.assertEqual(Encoder(123).encode(), b'i123e')

    def test_encode_str(self):
        self.assertEqual(Encoder('Hello World!').encode(), b'12:Hello World!')

    def test_encode_list(self):
        self.assertEqual(Encoder([1, 2, 3]).encode(), b'li1ei2ei3ee')

    def test_encode_orderddict(self):
        mydict = OrderedDict()
        mydict['town'] = 'New York'
        mydict['name'] = 'Ereboras'
        mydict['age'] = 3
        self.assertEqual(Encoder(mydict).encode(), b'd4:town8:New York4:name8:Ereboras3:agei3ee')

    def test_encode_error_type(self):
        self.assertRaises(TypeError, Encoder, tuple)

    def test_encode_list_error_type(self):
        mylist = [1, 2, tuple]
        self.assertRaises(TypeError, Encoder(mylist).encode)

    def test_encode_dict_error_type(self):
        mydict = OrderedDict()
        mydict['town'] = 'New York'
        mydict['name'] = tuple
        mydict['age'] = 3
        self.assertRaises(TypeError, Encoder(mydict).encode)

    def test_encode_dict_error_type_key(self):
        mydict = OrderedDict()
        mydict['town'] = 'New York'
        mydict[123] = 'Ereboras'
        mydict['age'] = 3
        self.assertRaises(TypeError, Encoder(mydict).encode)

    def test_decode_int(self):
        self.assertEqual(Decoder(b'i123e').decode(), 123)

    def test_decode_int_error_end(self):
        self.assertRaises(EOFError, Decoder(b'i123').decode)

    def test_decode_str(self):
        self.assertEqual(Decoder(b'12:Hello World!').decode(), b'Hello World!')

    def test_decode_str_error_end(self):
        self.assertRaises(EOFError, Decoder(b'15:Hello World!').decode)

    def test_decode_list(self):
        self.assertEqual(Decoder(b'l12:Hello World!i123e3:youe').decode(), [b'Hello World!', 123, b'you'])

    def test_decode_dict(self):
        mydict = OrderedDict()
        mydict[b'town'] = b'New York'
        mydict[b'123'] = b'Ereboras'
        mydict[b'age'] = 3
        mydict[b'list'] = [b'Hello World!', 123, b'you']
        self.assertEqual(Decoder(b'd4:town8:New York3:1238:Ereboras3:agei3e4:listl12:Hello World!i123e3:youee').decode(), mydict)

    def test_decode_dict_error_type_key(self):
        mydict = OrderedDict()
        mydict[b'town'] = b'New York'
        mydict[123] = b'Ereboras'
        mydict[b'age'] = 3
        mydict[b'list'] = [b'Hello World!', 123, b'you']
        self.assertRaises(TypeError, Decoder(b'd4:town8:New Yorki123e8:Ereboras3:agei3e4:listl12:Hello World!i123e3:youee').decode)