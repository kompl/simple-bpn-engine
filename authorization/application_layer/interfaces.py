from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from uuid import UUID


class UserIn(CamelModel):
    user_name: str
    password: str


class UserOut(CamelModel):
    uid: UUID
    user_name: str
    disabled: bool


class TokenOut(BaseModel):
    access_token: str
    token_type: str
