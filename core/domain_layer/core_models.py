from database_utils.base_db_model import BaseDBModel
import uuid as uuid_lib
import datetime


class BoardDB(BaseDBModel):
    __table__ = 'boards'
    __pk__ = 'uuid'

    uuid: uuid_lib.UUID
    name: str
    description: str
    status_id: int


class MethodDB(BaseDBModel):
    __table__ = 'method'
    __pk__ = 'uuid'

    uuid: uuid_lib.UUID
    name: str
    description: str
    enabled: bool
    status_id: int
    next_method_uuid: uuid_lib.UUID
    prev_method_uuid: uuid_lib.UUID


class MethodStatusDB(BaseDBModel):
    __table__ = 'method_statuses'
    __pk__ = 'id'

    id: int
    name: str
    description: str


class PlaneJobMethodConfigDB(BaseDBModel):
    __table__ = 'plane_job_method_config'
    __pk__ = 'uuid'

    uuid: uuid_lib.UUID
    method_uuid: uuid_lib.UUID
    plane_execution_date_time: datetime.datetime
    completed: bool


class PeriodicJobConfigDB(BaseDBModel):
    __table__ = 'periodic_job_config'
    __pk__ = 'uuid'

    uuid: uuid_lib.UUID
    method_uuid: uuid_lib.UUID
    interval: int
    last_call: datetime.datetime


class HTTPMethodConfigDB(BaseDBModel):
    __table__ = ''
    __pk__ = ''

    uuid: uuid_lib.UUID
    method_uuid: uuid_lib.UUID
    uri_pattern: str
    method: str
    body: str
    headers: str
    expected_response_uuid: uuid_lib.UUID


class HTTPResponseDB(BaseDBModel):
    __table__ = ''
    __pk__ = ''

    uuid: uuid_lib.UUID
    status: int
    body: str
    headers: str
