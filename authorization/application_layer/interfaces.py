from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from uuid import UUID
from typing import List


class UserIn(CamelModel):
    user_name: str
    password: str


class UserOut(CamelModel):
    uid: UUID
    user_name: str
    disabled: bool
    available_boards: List[UUID]


class TokenOut(BaseModel):
    access_token: str
    token_type: str
