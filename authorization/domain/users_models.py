from uuid import UUID
from typing import Optional
from fastapi_async_db_utils import BaseDBModel


class UserDB(BaseDBModel):
    __table__ = 'users'
    __pk__ = 'uid'

    uid: Optional[UUID]
    user_name: str
    disabled: Optional[bool]
    hashed_password: Optional[str]
