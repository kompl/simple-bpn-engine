from fastapi_camelcase import CamelModel
from uuid import UUID
from typing import Optional
from abc import ABC, abstractmethod


class AbstractMeta(ABC):

    @property
    @abstractmethod
    def table(self):
        return self.table


    @property
    @abstractmethod
    def pk(self):
        return self.pk


class UserDB(CamelModel):
    uid: Optional[UUID]
    user_name: str
    disabled: Optional[bool]
    hashed_password: Optional[str]

    class Meta(AbstractMeta):
        table = 'users'
        pk = 'uid'
