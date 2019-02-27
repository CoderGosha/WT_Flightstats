import unittest

from Fly.models.flight_info_status_request import FlightInfoStatusRequest
from Fly.services.flight_service import FlightService


class FlightServiceTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_one_fly(self):
        fly_request = FlightInfoStatusRequest(carrier="D2", flight="020", year="2019", month="02", day="27")
        service = FlightService()
        response = service.get_one_fly(fly_request)

        self.assertIsNotNone(response)
