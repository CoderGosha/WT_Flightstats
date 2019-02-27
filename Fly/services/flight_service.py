import json
import logging
from collections import namedtuple

import requests
from injector import Injector

from Fly.models.flight_info_status_request import FlightInfoStatusRequest
from Fly.models.storage_model import FlightStatusModel
from configuration import Configuration


class FlightService:
    def __init__(self):
        injector = Injector()
        configuration = injector.get(Configuration)
        self.fxmlUrl = configuration.config['DEFAULT']['FLIGHT_URL']
        self.app_id = configuration.config['DEFAULT']['FLIGHT_ID']
        self.apiKey = configuration.config['DEFAULT']['FLIGHT_KEY']

    def get_one_fly(self, fly_request: FlightInfoStatusRequest) -> FlightStatusModel:

        url = "flight/status/{0}/{1}/arr/{2}/{3}/{4}".format(fly_request.carrier, fly_request.flight, fly_request.year,
                                                             fly_request.month, fly_request.day)
        params = {"appId": self.app_id, "appKey": self.apiKey}
        response = requests.get(self.fxmlUrl + url, params=params,
                                )
        result = json.loads(response.text, object_hook=lambda d: namedtuple('FlightInfoStatusResponse',
                                                                            d.keys())(*d.values()))

        if response.status_code != 200:
            logging.error(response.text)

        status_flight = FlightStatusModel()
        status_flight.status = result.flightStatuses[0].status
        status_flight.departure_airport_fs_code = result.flightStatuses[0].departureAirportFsCode
        status_flight.arrival_airport_fs_code = result.flightStatuses[0].arrivalAirportFsCode
        status_flight.departure_date = result.flightStatuses[0].departureDate.dateLocal
        status_flight.arrival_date = result.flightStatuses[0].arrivalDate.dateLocal
        status_flight.published_departure = result.flightStatuses[0].operationalTimes.publishedDeparture.dateLocal
        status_flight.departure_terminal = result.flightStatuses[0].airportResources.departureTerminal
        status_flight.equipments_name = result.appendix.equipments[0].name

        for airport in result.appendix.airports:
            if status_flight.arrival_airport_fs_code == airport.fs:
                status_flight.arrival_airport_name = airport.name
                status_flight.arrival_airport_city = airport.city
                status_flight.arrival_airport_country = airport.countryName

            if status_flight.departure_airport_fs_code == airport.fs:
                status_flight.departure_airport_name = airport.name
                status_flight.departure_airport_city = airport.city
                status_flight.departure_airport_country= airport.countryName

        logging.info("Get status %s" % str(status_flight))

        return status_flight

