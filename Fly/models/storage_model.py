import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
DeclarativeBase = declarative_base()


class FlightStatusModel(DeclarativeBase):
    __tablename__ = "FlightStatus"
    id = Column(Integer, primary_key=True)
    time_update = Column('time_update', String)
    flight_departure = Column('flight_departure', String)
    flight_number = Column('flight_number', String)

    arrival_airport_fs_code = Column('arrival_airport_fs_code', String)
    departure_airport_fs_code = Column('departure_airport_fs_code', String)
    departure_date = Column('departure_date', String)
    arrival_date = Column('arrival_date', String)
    published_departure = Column('published_departure', String)
    status = Column('status', String)
    departure_terminal = Column('departure_terminal', String)
    arrival_airport_name = Column('arrival_airport_name', String)
    arrival_airport_city = Column('arrival_airport_city', String)
    arrival_airport_country = Column('arrival_airport_country', String)
    departure_airport_name = Column('departure_airport_name', String)
    departure_airport_city = Column('departure_airport_city', String)
    departure_airport_country = Column('departure_airport_country', String)
    equipments_name = Column('equipments_name', String)

    def decode_status(self):
        if self.status == "A":
            return "Active"
        elif self.status == "C":
            return "Canceled"
        elif self.status == "D":
            return "Diverted"
        elif self.status == "DN":
            return "Data source needed"
        elif self.status == "L":
            return "Landed"
        elif self.status == "NO":
            return "Not Operational"
        elif self.status == "R":
            return "Redirected"
        elif self.status == "S":
            return "Scheduled"
        else:
            return "Unknown"

    @staticmethod
    def convert_datetime(dt):
        return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f")

    def __str__(self):
        msg = str.format("Рейс {0}. Вылет: {1}-{2}. Прилет: {3}-{4}. Самолет: {5}",
                         self.flight_number, self.departure_airport_city, self.departure_date,
                         self.arrival_airport_city, self.arrival_date, self.equipments_name)
        return msg

    def __eq__(self, other):
        result = True
        field_pass = ["id", "time_update", "_sa_instance_state"]

        for item in self.__dict__:
            if item in field_pass:
                continue

            if str(self.__dict__[item]) == str(other.__dict__[item]):
                pass
            else:
                result = False

        return result
