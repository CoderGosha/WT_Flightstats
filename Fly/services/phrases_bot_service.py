import json
import logging
from collections import namedtuple

import requests
from injector import Injector

from configuration import Configuration


class PhrasesBotService:
    def __init__(self):
        injector = Injector()
        configuration = injector.get(Configuration)

        self.secret_key = configuration.config['DEFAULT']['SECRET']
        self.api_url = configuration.config['DEFAULT']['URL']
        self.url_get_avia = self.api_url + "/api/v1/phrases-bot"

    def get_bind(self, bind_bot)->str:
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Content-Encoding': 'utf-8',
                   'Authorization': 'Token %s' % self.secret_key}
        params = {"bind_bot": bind_bot}
        answer = requests.get(self.url_get_avia, headers=headers, params=params)
        result = json.loads(answer.text, object_hook=lambda d: namedtuple('AviaSubscription', d.keys())(*d.values()))

        if answer.status_code != 200:
            logging.error(answer.text)

        return result.name_ru
