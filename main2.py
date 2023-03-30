from serialsimple import SerialLogger

def main():
    logger = SerialLogger(port='/dev/ttyACM0', baudrate=115200, log_interval_sec=5, log_directory='logfiles', zip_directory='zipfiles')
    logger.start_logging()

if __name__ == '__main__':
    main()
