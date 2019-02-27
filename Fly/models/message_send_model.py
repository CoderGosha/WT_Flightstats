import json


class MessageSendModel:
    def __init__(self, id, platform, text=None, time="1"):
        self.id = id
        self.platform = platform
        self.text = text
        self.time = time
