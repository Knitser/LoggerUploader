from serialsimple import SerialLogger

logger = SerialLogger(port='/dev/ttyACM0', baudrate=115200, log_interval_sec=120, log_directory='logfiles')
logger.start_logging()