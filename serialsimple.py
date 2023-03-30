import serial
import time
import os

class SerialLogger:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200, log_interval_sec=120, log_directory='logfiles'):
        self.port = port
        self.baudrate = baudrate
        self.log_interval_sec = log_interval_sec
        self.log_directory = log_directory

        # Create a new directory for the log files if it doesn't exist
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def start_logging(self):
        # Create a new serial object
        ser = serial.Serial(self.port, self.baudrate)

        # Create a new log file
        log_filename = self._get_log_filename()
        log_file = open(log_filename, 'w')

        # set the start time
        start_time = time.time()

        try:
            while True:
                line = ser.readline().decode('utf-8').strip()
                print(line)

                # write the data to the log file
                log_file.write(line + '\n')

                # check if log interval has passed
                if time.time() - start_time >= self.log_interval_sec:
                    # close the current log file
                    log_file.close()

                    # create a new log filename based on the current time
                    new_log_filename = self._get_log_filename()

                    # rename the current log file to the new filename
                    os.rename(log_filename, new_log_filename)

                    # open a new log file for writing
                    log_file = open(log_filename, 'w')

                    # reset the start time
                    start_time = time.time()

        except KeyboardInterrupt:
            ser.close()
            log_file.close()

    def _get_log_filename(self):
        return os.path.join(self.log_directory, time.strftime("%Y-%m-%d_%H-%M-%S_logfile.asc", time.localtime()))


logger = SerialLogger(port='/dev/ttyACM0', baudrate=115200, log_interval_sec=120, log_directory='logfiles')
logger.start_logging()
