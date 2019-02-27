from datetime import datetime


class FlightInfoStatusRequest:
    def __init__(self, carrier, flight, year, month, day):
        self.carrier = carrier
        self.flight = flight
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    def convert_subscription(flight_number, flight_departure):
        flight_dep = datetime.utcfromtimestamp(flight_departure)
        f_car = None
        f_num = None
        if len(flight_number) == 5:
            f_car = flight_number[:2]
            f_num = flight_number[2:]

        if len(flight_number) == 6:
            try:
                int(flight_number[2])
                f_car = flight_number[:2]
                f_num = flight_number[2:]
            except:
                f_car = flight_number[:3]
                f_num = flight_number[2:]

        return FlightInfoStatusRequest(carrier=f_car, flight=f_num, year=flight_dep.year, month=flight_dep.month,
                                       day=flight_dep.day)


