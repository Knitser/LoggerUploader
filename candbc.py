import can
import cantools

# command: echo -e 'vcan0  214   [8]  80 4A 0F 00 00 00 00 00 ::' | python3 -m cantools decode motohawk.dbc

db = cantools.database.load_file('motohawk.dbc')
line = b'  15.706331 2  08A        Rx D 7 A1  71  0  73  43  11  6C'
line.split()
print(line)
#   15.706331 2  08A        Rx D 7 A1  71  0  73  43  11  6C

# can_bus = can.interface.Bus('vcan0', bustype='socketcan')
# message = can.Message(arbitration_id=0x214, data=b'\x80\x4A\x0F\x00\x00\x00\x00\x00')
decoded_data = db.decode_message(0x214, b'\x80\x4A\x0F\x00\x00\x00\x00\x00')
print(decoded_data)
