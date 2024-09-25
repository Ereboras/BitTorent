import unittest
from collections import OrderedDict
from pieces.bencode import Encoder

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