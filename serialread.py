import serial

# Define the serial port settings
# port = 'COM1'
port = '/dev/ttyUSB0'
baudrate = 115200

# Create a new serial object
ser = serial.Serial(port, baudrate)
# ser = serial.Serial('/dev/ttyAMA0', 115200)

while True:
    try:
        line = ser.readline()

        # Decode the bytes into a string
        # line = line.decode('utf-8').strip()

        print(line)
    except KeyboardInterrupt:
        ser.close()
        break
