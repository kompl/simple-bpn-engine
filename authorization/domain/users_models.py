from uuid import UUID
from typing import Optional
from database_utils.base_db_model import BaseDBModel


class UserDB(BaseDBModel):
    __table__ = 'users'
    __pk__ = 'uid'

    uid: Optional[UUID]
    user_name: str
    disabled: Optional[bool]
    hashed_password: Optional[str]

