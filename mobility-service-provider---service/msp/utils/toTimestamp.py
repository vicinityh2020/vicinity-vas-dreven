import datetime
import time

def to_timestamp(value):
    return int(value.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)

def to_timestamp_ms():
    return int(time.time() * 1000)

def to_datetime(value):
    return datetime.utcfromtimestamp(value)