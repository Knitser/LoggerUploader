import serial
import time
import os
import gzip

class SerialLogger:
    def __init__(self, port, baudrate, log_interval_sec, log_directory, zip_directory):
        self.port = port
        self.baudrate = baudrate
        self.log_interval_sec = log_interval_sec
        self.log_directory = log_directory
        self.zip_directory = zip_directory

        # Create a new directory for the log files if it doesn't exist
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        # Create a new directory for the zip files if it doesn't exist
        if not os.path.exists(self.zip_directory):
            os.makedirs(self.zip_directory)

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

                    # zip the old log file
                    self.zip_log_file(new_log_filename)

                    # open a new log file for writing
                    log_file = open(log_filename, 'w')

                    # reset the start time
                    start_time = time.time()

        except KeyboardInterrupt:
            ser.close()
            log_file.close()

    def _get_log_filename(self):
        return os.path.join(self.log_directory, time.strftime("%Y-%m-%d_%H-%M-%S_logfile.asc", time.localtime()))

    def zip_log_file(self, log_filename):
        # create the gzip filename based on the log filename
        gzip_filename = os.path.splitext(os.path.basename(log_filename))[0] + '.gz'

        # open the log file for reading
        with open(log_filename, 'rb') as f_in:
            # create the gzip file for writing
            with gzip.open(os.path.join(self.zip_directory, gzip_filename), 'wb') as f_out:
                f_out.writelines(f_in)

        # delete the log file
        os.remove(log_filename)
