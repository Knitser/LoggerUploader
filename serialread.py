import serial
import logging
import time

# Define the serial port settings
# port = 'COM1'
port = '/dev/ttyUSB0'
baudrate = 115200

# Configure the logger to write to a file in the logfiles directory
# logging.basicConfig(filename='logfiles/logfile.asc', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Create a new serial object
ser = serial.Serial(port, baudrate)

while True:
    try:
        line = ser.readline()

        # Decode the bytes into a string
        line = line.decode('utf-8').strip()

        # Write the line to the log file
        logging.info(line)

        print(line)

        # Sleep for 2 minutes
        time.sleep(120)

    except KeyboardInterrupt:
        ser.close()
        break
