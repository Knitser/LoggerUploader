from logger import SerialLogger
from datetime import datetime


def main():
    port = '/dev/ttyACM0'
    baudrate = 115200
    log_interval_sec = 5
    log_directory = 'logfiles'
    zip_directory = 'zipfiles'
    bucket_name = 'blackboxlinkedcar'
    s3_prefix = datetime.now().strftime('logfiles/%Y/%m/%d/%H/')

    logger = SerialLogger(port, baudrate, log_interval_sec, log_directory, zip_directory, bucket_name, s3_prefix)
    logger.start_logging()

    # create logic between cloud EOS commands and Serial commands
    # logger.send_command('phase_1')

    # echo -e 'vcan0  1F0   [8]  80 4A 0F 00 00 00 00 00 ::' | python3 -m cantools decode tests/files/dbc/motohawk.dbc


if __name__ == '__main__':
    main()
