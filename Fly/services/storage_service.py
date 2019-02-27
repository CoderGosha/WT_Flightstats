import datetime

from injector import Injector
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from Fly.models.storage_model import DeclarativeBase, FlightStatusModel
from configuration import Configuration


class StorageService:
    def __init__(self):
        injector = Injector()
        configuration = injector.get(Configuration)
        self.database = configuration.config['DEFAULT']['DATABASE']
        self.sessions = {}

        self.engine = self.create_engine()
        self.create_tables(self.engine)

    def create_engine(self):
        engine = create_engine(URL(**self.database), poolclass=NullPool, encoding="utf8")
        return engine

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine)()
        return session

    def is_first(self, id, flight_departure, flight_number) -> bool:
        session = self.create_session(self.engine)
        result = session.query(FlightStatusModel).filter_by(id=id).first()
        if result is None:
            status = FlightStatusModel()
            status.id = id
            status.flight_number = flight_number
            status.flight_departure = flight_departure
            session.add(status)
            session.commit()
            return True
        else:
            return False

    def get_last_update(self, id):
        session = self.create_session(self.engine)
        result = session.query(FlightStatusModel).filter_by(id=id).first()
        return result.time_update

    def get_id(self, id):
        session = self.create_session(self.engine)
        return session.query(FlightStatusModel).get(id)

    def update_time(self, flight_departure, flight_number):
        # Обновим тайм у всех кто попадает под критерии
        session = self.create_session(self.engine)
        timenow = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).timestamp()
        session.query(FlightStatusModel).filter_by(flight_departure=flight_departure). \
            filter_by(flight_number=flight_number). \
            update({"time_update": timenow})

        session.commit()
        session.close()

    def update_status(self, status_flight: FlightStatusModel):
        # Выберем все по рейсу и департации и обновим
        session = self.create_session(self.engine)
        timenow = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).timestamp()
        session.query(FlightStatusModel).filter_by(flight_departure=status_flight.flight_departure). \
            filter_by(flight_number=status_flight.flight_number). \
            update(
            {"time_update": timenow,
             "departure_airport_fs_code": status_flight.departure_airport_fs_code,
             "arrival_airport_fs_code": status_flight.arrival_airport_fs_code,
             "departure_date": status_flight.departure_date,
             "arrival_date": status_flight.arrival_date,
             "published_departure": status_flight.published_departure,
             "status": status_flight.status,
             "departure_terminal": status_flight.departure_terminal,
             "arrival_airport_name": status_flight.arrival_airport_name,
             "arrival_airport_city": status_flight.arrival_airport_city,
             "arrival_airport_country": status_flight.arrival_airport_country,
             "departure_airport_name": status_flight.departure_airport_name,
             "departure_airport_city": status_flight.departure_airport_city,
             "departure_airport_country": status_flight.departure_airport_country,
             "equipments_name": status_flight.equipments_name,

             })

        session.commit()
        session.close()
