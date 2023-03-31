import json

config = {
  "aws": {
    "aws_credentials_folder": "~/.aws/credentials"
  },
  "app": {
    "start_delay": 0.1,
    "log_split": 2000000,
    "log_file_path": "/logfiles",
    "zip_file_path": "/zipfiles"
  },
  "log_channel": {
    "can": 2,
    "obd": 1
  },
  "logging": {
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 115200,
    "log_interval": 120,
    "log_file_path": "/logfiles"
  }
}

class Helpers:

    @staticmethod
    def load_config():
        # Load config
        with open('config.json') as config_file:
            config = json.load(config_file)
        return config
    
    
