from fastapi_async_db_utils.crud import create, delete_by_params, update_by_params
from abc import ABC, abstractmethod
from core.infrastructure_layer.list_selections import select_board_list


class CRUDService(ABC):

    @property
    @abstractmethod
    def interfaces_factory(self):
        return self.interfaces_factory

    @property
    @abstractmethod
    def select_list_coroutine(self):
        return self.select_list_coroutine

    @property
    @abstractmethod
    def select_detail_coroutine(self):
        return self.select_detail_coroutine

    def __init__(self):
        self._interfaces_factory = self.interfaces_factory()
        self.conn = None

    def setup(self, conn):
        self.conn = conn

    async def read_list(self, *table_params, **filters):
        db_raw_data = await self.select_list_coroutine.__func__(self.conn, table_params, filters)
        return [self._interfaces_factory.create_output_list_model_object(row) for row in db_raw_data]

    async def read_detail(self, primary_key):
        db_raw_data = await self.select_detail_coroutine.__func__(self.conn, primary_key)
        return self._interfaces_factory.create_output_model_object(db_raw_data)

    async def create(self, input_model_object, **extra_fields):
        db_model_object = self._interfaces_factory.create_db_model_object(input_model_object, **extra_fields)
        return await create(self.conn, db_model_object)

    async def update(self, input_model_object, filters: dict = None, excluded: tuple = tuple(), **extra_fields):
        filters = filters or {}
        db_model_object = self._interfaces_factory.create_db_model_object(input_model_object, **extra_fields)
        return await update_by_params(self.conn, db_model_object, *excluded, **filters)

    async def delete(self, **filters):
        db_model_object = self._interfaces_factory.db_model()
        return await delete_by_params(self.conn, db_model_object, **filters)
