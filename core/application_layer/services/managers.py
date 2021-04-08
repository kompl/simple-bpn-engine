from fastapi_async_db_utils.base_data_managers import CRUDService
from core.infrastructure_layer.list_selections import select_board_list
from core.infrastructure_layer.detail_selections import select_board
from core.application_layer.services.interfaces_factories import BoardInterfacesFactory



class BoardService(CRUDService):
    interfaces_factory = BoardInterfacesFactory
    select_list_coroutine = select_board_list
    select_detail_coroutine = select_board

    async def read_available_board_detail(self, primary_key, user_uuid):
        board = await super().read_detail(primary_key)
        if board.user_uid != user_uuid:
            raise Exception


