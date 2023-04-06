import re
import cantools

# command: echo -e 'vcan0  214   [8]  80 4A 0F 00 00 00 00 00 ::' | python3 -m cantools decode motohawk.dbc

db = cantools.database.load_file('motohawk.dbc')

mystring = "  0.350730 2  214       Rx D 8  80  4A  0F  00  00  00  00  00"
mystring = re.sub(' +', ' ', mystring)
mylist = mystring.split(" ")
dataLenght = int(mylist[6], 10)
data = bytearray.fromhex(''.join(mylist[-dataLenght::1]))
id = int(mylist[3], 16)
print(f'CAN ID')
print(hex(id))
print(f'Message data')
print(f' '.join(hex(byte) for byte in data))
decoded_data = db.decode_message(id, data)
print(f'Decoded data')
print(f'{decoded_data}')

