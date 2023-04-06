import json


class helpers:
    @staticmethod
    def load_config():
        with open('config.json') as config_file:
            config = json.load(config_file)
        return config