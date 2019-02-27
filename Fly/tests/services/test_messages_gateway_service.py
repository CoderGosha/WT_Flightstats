import datetime
import unittest

from Fly.models.message_send_model import MessageSendModel
from Fly.services.messages_gateway_service import MessagesGatewayService


class MessagesGatewayTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_send_message(self):
        msg_service = MessagesGatewayService()
        message = MessageSendModel("295641973", "tg", "TestMessage", "Test")
        status = msg_service.send_message(message=message)
        self.assertEqual(status, 201, "Error send")
