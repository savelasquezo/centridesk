from datetime import datetime

from pytz import timezone


def get_timestamp():
    return int(datetime.now(timezone('Europe/Madrid')).timestamp())


def from_timestamp_to_date(value, time_zone='Europe/Madrid'):

    if value:
        datetime_time_zone = datetime.fromtimestamp(value)
        output = datetime_time_zone.astimezone(timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')

    else:
        output = value

    return output
