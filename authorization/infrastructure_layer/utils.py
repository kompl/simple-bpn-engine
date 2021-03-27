import datetime
import os
import pytz


def get_timestamp():
    return datetime.datetime.now(tz=pytz.timezone(os.getenv('TZ')))


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class DoesNotExistError(Exception):
    pass
