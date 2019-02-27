import json
import os

from injector import singleton


class Configuration:
    config = None

    @singleton
    def __init__(self):
        filename = os.path.abspath(__file__).replace(__name__ + ".py", "") + "config.json"
        with open(filename, 'r') as f:
            self.config = json.load(f)
