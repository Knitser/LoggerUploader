import serial
import time
import os
import gzip
from upload_s3 import S3Uploader


class SerialLogger:
    def __init__(self, port, baudrate, log_interval_sec, log_directory, zip_directory, bucket_name, s3_prefix):
        self.port = port
        self.baudrate = baudrate
        self.log_interval_sec = log_interval_sec
        self.log_directory = log_directory
        self.zip_directory = zip_directory
        self.s3_uploader = S3Uploader(bucket_name, s3_prefix)

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        if not os.path.exists(self.zip_directory):
            os.makedirs(self.zip_directory)

    def _get_log_filename(self):
        return os.path.join(self.log_directory, time.strftime("%Y-%m-%d_%H-%M-%S_logfile.asc", time.gmtime()))

    def zip_logs(self, log_filename):
        zip_filename = os.path.join(self.zip_directory, os.path.basename(log_filename) + '.gz')
        with open(log_filename, 'rb') as f_in, gzip.open(zip_filename, 'wb', compresslevel=9) as f_out:
            f_out.writelines(f_in)

    def upload_and_delete_zip_files(self):
        for zip_file in os.listdir(self.zip_directory):
            zip_filepath = os.path.join(self.zip_directory, zip_file)
            self.s3_uploader.upload_file(zip_filepath)
            os.remove(zip_filepath)

    def start_logging(self):
        ser = serial.Serial(self.port, self.baudrate)

        log_filename = self._get_log_filename()
        log_file = open(log_filename, 'w')

        start_time = time.time()

        try:
            while True:
                line = ser.readline().decode('utf-8').strip()
                print(line)

                # write the data to the log file
                log_file.write(line + '\n')

                # check if log interval has passed
                if time.time() - start_time >= self.log_interval_sec:
                    log_file.close()

                    # zip the previous log file
                    self.zip_logs(log_filename)

                    log_filename = self._get_log_filename()
                    log_file = open(log_filename, 'w')

                    # reset the start time
                    start_time = time.time()

        except KeyboardInterrupt:
            ser.close()
            log_file.close()
