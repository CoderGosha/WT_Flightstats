import datetime
import unittest

from Fly.services.avia_subscription_service import AviaSubscriptionService


class AviaSubscriptionServiceTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_actual_subscription(self):
        service = AviaSubscriptionService()
        result = service.get_actual_subscriptions()
        self.assertIsNotNone(result)

