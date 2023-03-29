import serial
import logging
import time

class SerialLogger:
    def __init__(self, port, baudrate, log_interval, log_directory):
        self.port = port
        self.baudrate = baudrate
        self.log_interval = log_interval
        self.log_directory = log_directory

        # Configure the logger to write to a file in the logfiles directory
        self.start_logging()

    def start_logging(self):
        logging.basicConfig(filename=f'{self.log_directory}/logfile.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    def stop_logging(self):
        logging.shutdown()

    def split_logfile(self):
        logging.info('Splitting log file...')
        self.stop_logging()
        self.start_logging()

    def run(self):
        # Create a new serial object
        ser = serial.Serial(self.port, self.baudrate)

        # Initialize the time when the current log file was created
        start_time = time.time()

        while True:
            try:
                line = ser.readline()

                # Decode the bytes into a string
                line = line.decode('utf-8').strip()

                # Write the line to the log file
                logging.info(line)

                # Check if the log interval has elapsed since the log file was created
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time > self.log_interval:
                    # Split the log file
                    self.split_logfile()
                    start_time = current_time

            except KeyboardInterrupt:
                ser.close()
                self.stop_logging()
                break

