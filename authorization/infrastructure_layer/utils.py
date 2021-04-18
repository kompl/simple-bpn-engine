import datetime
import os
from zoneinfo import ZoneInfo

def get_timestamp():
    return datetime.datetime.now(tz=ZoneInfo(os.getenv('TZ')))
