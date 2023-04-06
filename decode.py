import re
import cantools

db = cantools.database.load_file('TeslaModel3.dbc')

mystring = "  0.350730 2  214       Rx D 8  80  4B  0F  4B  00  00  00  00"
mylist = re.split('\s+', mystring.strip())
data_length = int(mylist[5], 10)
data = bytearray.fromhex(''.join(mylist[-data_length::1]))
can_id = int(mylist[2], 16)

print(f'CAN ID: {hex(can_id)}')
print(f'Message data: {" ".join(hex(byte) for byte in data)}')

decoded_data = db.decode_message(can_id, data)
print(f'Decoded data: {decoded_data}')
