from fastapi_async_db_utils import CRUDService
from core.infrastructure_layer.list_selections import select_board_list
from core.infrastructure_layer.detail_selections import select_board
from core.application_layer.services.interfaces_factories import BoardInterfacesFactory


class BoardService(CRUDService):
    interfaces_factory = BoardInterfacesFactory
    select_list_coroutine = select_board_list
    select_detail_coroutine = select_board

    async def create_board(self, board_in, user_uid, **extra_fields):
        board = await super().create(board_in, **extra_fields)

