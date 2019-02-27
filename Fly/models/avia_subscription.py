from Fly.models.platform_account import PlatformAccount


class AviaSubscription:
    id = None
    flight_departure = None
    is_datetime_utc = None
    flight_number = None
    platform_account = PlatformAccount()
