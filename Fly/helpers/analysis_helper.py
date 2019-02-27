import logging
from datetime import datetime, timedelta

from Fly.models.avia_subscription import AviaSubscription


class AnalysisHelper:
    def is_update(self, subscription: AviaSubscription, last_update)-> bool:
        flight_departure = datetime.utcfromtimestamp(subscription.flight_departure)

        if flight_departure - timedelta(hours=80) > datetime.utcnow():
            # Смотрим рейсы ближе к 30 часам до вылета
            return False

        if last_update is None:
            return True
        else:
            try:
                dt_last_time = datetime.utcfromtimestamp(float(last_update))
            except ValueError:
                logging.warning("Convert DataTime Error: %s" % subscription.flight_number)
                return True

        if flight_departure - timedelta(hours=6) > datetime.utcnow():
            # От 30 часов до 6
            if dt_last_time - timedelta(minutes=30) > datetime.utcnow():
                return True
            else:
                return False

        elif flight_departure - timedelta(hours=4) > datetime.utcnow():
            # От 6 часов до 4
            if dt_last_time - timedelta(minutes=5) > datetime.utcnow():
                return True
            else:
                return False

        elif flight_departure > datetime.utcnow():
            return False
        else:
            return False
