from collections import OrderedDict
from pieces.bencode import Encoder

mydict = OrderedDict()
mydict['town'] = 'New York'
mydict['name'] = 'Ereboras'
mydict['age'] = 3

myint = 123

mystr = 'Hello world!'

mylist = [1,2,3]

print(Encoder(mylist).encode())