from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseDBModel(BaseModel, ABC):
    @property
    @abstractmethod
    def __table__(self):
        return self.__table__

    @property
    @abstractmethod
    def __pk__(self):
        return self.__pk__
