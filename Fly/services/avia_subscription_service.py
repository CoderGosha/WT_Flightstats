import json
import logging
from collections import namedtuple
from typing import List

import requests
from injector import Injector

from Fly.models.avia_subscription import AviaSubscription
from configuration import Configuration


class AviaSubscriptionService:
    def __init__(self):
        injector = Injector()
        configuration = injector.get(Configuration)

        self.secret_key = configuration.config['DEFAULT']['SECRET']
        self.api_url = configuration.config['DEFAULT']['URL']
        self.url_get_avia = self.api_url + "/api/v1/avia-subscriptions"

    def get_actual_subscriptions(self) -> List[AviaSubscription]:
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Content-Encoding': 'utf-8',
                   'Authorization': 'Token %s' % self.secret_key}

        answer = requests.get(self.url_get_avia, headers=headers)
        result = json.loads(answer.text, object_hook=lambda d: namedtuple('AviaSubscription', d.keys())(*d.values()))

        if answer.status_code != 200:
            logging.error(answer.text)

        return result

    @staticmethod
    def get_unic_subcription(subsriptions: List[AviaSubscription]) -> List[AviaSubscription]:
        result = []
        for item in subsriptions:
            if any(x for x in result if (x.flight_number == item.flight_number) and
                                        (x.flight_departure == item.flight_departure)):
                continue
            else:
                result.append(item)

        return result

    @staticmethod
    def get_subscraption_by_flight_number(subsriptions: List[AviaSubscription],
                                          flight_number, flight_departure) -> List[AviaSubscription]:
        result = []
        for item in subsriptions:
            if ((item.flight_number == flight_number)
                    and (item.flight_departure == flight_departure)):
                result.append(item)

        return result
