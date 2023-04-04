import time
import serial


def send_command(command):
    ser = serial.Serial('COM5', 115200)

    if command == 'can_speed_500k':
        ser.write(b'can,500\n')

    elif command == 'can_speed_250k':
        ser.write(b'can,250\n')

    elif command == 'phase_1':
        ser.write(b'phase,1\n')

    elif command == 'phase_2':
        ser.write(b'phase,2\n')

    elif command == 'filter_apply':
        ser.write(b'filter,1,200\n')

    elif command == 'filter_apply_range':
        ser.write(b'filter,1,200,300\n')

    elif command == 'filter_exclude':
        ser.write(b'filter,0,200\n')

    elif command == 'filter_exclude_range':
        ser.write(b'filter,0,200,300\n')

    print(ser.readline().decode('utf-8').strip())
    ser.close()


while True:
    send_command('can_speed_500k')
    time.sleep(5)
    send_command('filter_apply')
    time.sleep(5)


