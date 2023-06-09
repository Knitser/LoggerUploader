from datetime import datetime
from upload_s3 import S3Uploader
from oldfiles.logfilesplitter import LogfileSplitter
from logger import SerialLogger
import os
import subprocess


def main():
    # start the logger
    logger = SerialLogger(serial_port='/dev/ttyUSB0', baudrate=115200, log_interval=120, log_directory='logfiles')
    logger.start_logging()

    # changing variables
    file_format_aws = datetime.now().strftime('logfiles/%Y/%m/%d/%H/')
    file_size_2mb = 2 * 1024 * 1024

    s3_uploader = S3Uploader('blackboxlinkedcar', file_format_aws)
    logfiles = LogfileSplitter(file_size_2mb)

    # Create the zipfiles directory if it doesn't exist
    if not os.path.exists('zipfiles'):
        os.makedirs('zipfiles')

    # Delete the previous zip files
    for filename in os.listdir('zipfiles'):
        os.remove(os.path.join('zipfiles', filename))
        print('Old zipfiles successfully removed')

    # Split each logfile into smaller parts and upload them individually
    for filename in os.listdir('logfiles'):
        input_path = os.path.join('logfiles', filename)
        for chunk_path in logfiles.split_logfile(input_path):
            s3_uploader.upload_file(chunk_path)

    print('All logfiles successfully uploaded to S3')


if __name__ == '__main__':
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    main()
