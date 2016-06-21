from datetime import datetime
import pytz


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


def parse_datetime(s):
    if not s:
        return None
    return datetime.strptime(s, DATETIME_FORMAT).replace(tzinfo=pytz.utc)


def format_datetime(dt):
    return dt.astimezone(pytz.utc).strftime(DATETIME_FORMAT)


def format_date(d):
    return d.strftime(DATE_FORMAT)