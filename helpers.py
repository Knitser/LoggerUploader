import json


class Helpers:

    @staticmethod
    def on_exit(logfile, error_log):
        """close logfiles (and) canbus"""
        print("End Triggerblock", file=logfile)  # Save data to file
        logfile.close()
        error_log.close()

    @staticmethod
    def load_config():
        # Load config
        with open('/usr/src/app/config.json') as config_file:
            config = json.load(config_file)
        return config

    @staticmethod
    def load_cars_config():
        # Load config
        with open('/usr/src/app/cars.json') as cars:
            config = json.load(cars)
        return config

    def human_bytes(b):
        b = float(b)
        kb = float(1024)
        mb = float(kb ** 2)  # 1,048,576
        gb = float(kb ** 3)  # 1,073,741,824
        tb = float(kb ** 4)  # 1,099,511,627,776

        if b < mb:
            return '{0} {1}'.format(b, 'Bytes' if 0 == b > 1 else 'Byte')
        elif kb <= b < mb:
            return '{0:.2f} KB'.format(b / kb)
        elif mb <= b < gb:
            return '{0:.2f} MB'.format(b / mb)
        elif gb <= b < tb:
            return '{0:.2f} GB'.format(b / gb)
        elif tb <= b:
            return '{0:.2f} TB'.format(b / tb)
