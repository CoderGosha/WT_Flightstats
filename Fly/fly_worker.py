import json
import logging
import time

from Fly.helpers.analysis_helper import AnalysisHelper
from Fly.helpers.message_helper import MessageHelper
from Fly.models.flight_info_status_request import FlightInfoStatusRequest
from Fly.models.message_send_model import MessageSendModel
from Fly.services.avia_subscription_service import AviaSubscriptionService
from Fly.services.flight_service import FlightService
from Fly.services.storage_service import StorageService


class FlyWorker:
    def __init__(self):
        self.avia_sub_service = AviaSubscriptionService()
        self.storage_service = StorageService()
        self.message_helper = MessageHelper()
        self.analysis_helper = AnalysisHelper()
        self.flight_service = FlightService()

    def do(self):
        # Запрашиваем данные по всем актуальным рейсам
        all_subscriptions = self.avia_sub_service.get_actual_subscriptions()
        for subscription in all_subscriptions:
            # Проверим есть ли такой в БД

            if self.storage_service.is_first(subscription.id, subscription.flight_departure, subscription.flight_number):
                message = MessageSendModel(id=subscription.platform_account.platform_id,
                                           platform=subscription.platform_account.messenger_type)
                self.message_helper.hello_message(message, subscription.flight_departure, subscription.flight_number)

        for subscription in self.avia_sub_service.get_unic_subcription(all_subscriptions):
            # Смотрим уникальные подписки

            if self.analysis_helper.is_update(subscription, self.storage_service.get_last_update(subscription.id)):
                fly_request = FlightInfoStatusRequest.convert_subscription(subscription.flight_number,
                                                                           subscription.flight_departure)
                status_flight = self.flight_service.get_one_fly(fly_request)
                status_flight.flight_number = subscription.flight_number
                status_flight.flight_departure = subscription.flight_departure

                if status_flight != self.storage_service.get_id(subscription.id):
                    self.storage_service.update_status(status_flight)
                    self.message_helper.new_status(status_flight, all_subscriptions)
                    logging.info("Send Info " + str(status_flight))
                else:
                    self.storage_service.update_time(subscription.flight_departure, subscription.flight_number)

    def do_worker(self):
        logging.info("Starting Fly Service")
        while True:
            self.do()
            time.sleep(30)

