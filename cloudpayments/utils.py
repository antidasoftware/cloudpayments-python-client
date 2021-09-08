from datetime import datetime
import pytz


IN_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
OUT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT = "%Y-%m-%d"


def parse_datetime(s):
    if not s:
        return None
    return datetime.strptime(s, IN_DATETIME_FORMAT).replace(tzinfo=pytz.utc)


def format_datetime(dt):
    return dt.astimezone(pytz.utc).strftime(OUT_DATETIME_FORMAT)


def format_date(d):
    return d.strftime(DATE_FORMAT)
