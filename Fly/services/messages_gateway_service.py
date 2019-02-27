import json
import logging

import requests
from injector import Injector
from Fly.models.message_send_model import MessageSendModel
from configuration import Configuration


class MessagesGatewayService:
    def __init__(self):
        injector = Injector()
        configuration = injector.get(Configuration)

        self.secret_key = configuration.config['DEFAULT']['SECRET']
        self.api_url = configuration.config['DEFAULT']['URL']
        self.url_send = self.api_url + "/api/v1/subscriptions-queue"

    def send_message(self, message: MessageSendModel):
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Content-Encoding': 'utf-8',
                   'Authorization': 'Token %s' % self.secret_key}

        answer = requests.post(self.url_send, headers=headers, data=json.dumps(message.__dict__))
        if answer.status_code != 201:
            logging.error(answer.text)

        return answer.status_code
