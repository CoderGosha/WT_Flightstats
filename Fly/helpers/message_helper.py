import json
from datetime import datetime

from Fly.models.message_send_model import MessageSendModel
from Fly.models.storage_model import FlightStatusModel
from Fly.services.avia_subscription_service import AviaSubscriptionService
from Fly.services.messages_gateway_service import MessagesGatewayService
from Fly.services.phrases_bot_service import PhrasesBotService


class MessageHelper:
    def __init__(self):
        self.gateway_service = MessagesGatewayService()
        self.phrases_bot_service = PhrasesBotService()

    def hello_message(self, message: MessageSendModel, date, id):
        # Запросить текст первого сообщения
        text = self.phrases_bot_service.get_bind("fly_hello")
        message.text = text.format(id, datetime.utcfromtimestamp(date).strftime('%Y-%m-%d'))
        self.gateway_service.send_message(message)

    def new_status(self, status_flight: FlightStatusModel, all_subscriptions):
        """
            Обновилась информация о полете {flight_number}:
            Вылет: {departure_date} {departure_airport_name}, {departure_airport_city}, {departure_airport_country}
            Терминал вылета: {departure_terminal}
            Прилет:{arrival_date} {arrival_airport_name}, {arrival_airport_city}, {arrival_airport_country}
            Статус: {status}
            Самолет: {equipments_name}
        :param status_flight:
        :param all_subscriptions:
        :return:
        """
        departure_date = FlightStatusModel.convert_datetime(status_flight.departure_date).strftime('%Y-%m-%d %H:%M')
        arrival_date = FlightStatusModel.convert_datetime(status_flight.arrival_date).strftime('%Y-%m-%d %H:%M')

        # Разошлем сообщение по всем подписотчикам
        pattern = self.phrases_bot_service.get_bind("fly_update")
        text = pattern.format(flight_number=status_flight.flight_number, departure_date=departure_date,
                              departure_airport_name=status_flight.departure_airport_name,
                              departure_airport_city=status_flight.departure_airport_city,
                              departure_airport_country=status_flight.departure_airport_country,
                              departure_terminal=status_flight.departure_terminal,
                              arrival_date=arrival_date,
                              arrival_airport_name=status_flight.arrival_airport_name,
                              arrival_airport_city=status_flight.arrival_airport_city,
                              arrival_airport_country=status_flight.arrival_airport_country,
                              status=status_flight.decode_status(),
                              equipments_name=status_flight.equipments_name)

        current_subscriptions = AviaSubscriptionService.get_subscraption_by_flight_number(all_subscriptions,
                                                                                          flight_number=status_flight.flight_number,
                                                                                          flight_departure=status_flight.flight_departure)
        for user in current_subscriptions:
            message = MessageSendModel(id=user.platform_account.platform_id,
                                       platform=user.platform_account.messenger_type, text=text)
            self.gateway_service.send_message(message)
