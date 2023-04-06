from logger import SerialLogger
from datetime import datetime
from loadconfig import helpers

cfg = helpers.load_config()

def main():
    port = cfg['log']['serial_port']
    baudrate = cfg['log']['baudrate']
    log_interval_sec = cfg['log']['log_interval']
    log_directory = cfg['log']['log_file_path']
    zip_directory = cfg['log']['zip_file_path']
    bucket_name = cfg['log']['s3_bucket_name']
    s3_prefix = datetime.now().strftime(cfg['log']['s3_prefix'])
    upload_time_sec = cfg['log']['s3_bucket_name']

    logger = SerialLogger(port, baudrate, log_interval_sec, log_directory, zip_directory, bucket_name, s3_prefix, upload_time_sec)
    logger.start_logging()

    # create logic between cloud EOS commands and Serial commands
    # logger.send_command('phase_1')


if __name__ == '__main__':
    main()
