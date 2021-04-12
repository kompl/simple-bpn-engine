from fastapi_async_utils import CRUDService
from core.infrastructure_layer.list_selections import select_board_list
from core.infrastructure_layer.detail_selections import select_board
from core.infrastructure_layer.custom_crud_utils import create_boards_user_relation
from core.application_layer.services.interfaces_factories import BoardInterfacesFactory
from authorization.infrastructure_layer.exceptions import ForbiddenError


class BoardService(CRUDService):
    interfaces_factory = BoardInterfacesFactory
    select_list_coroutine = select_board_list
    select_detail_coroutine = select_board

    async def read_detail(self, primary_key, *args):
        try:
            return await super().read_detail(primary_key, *args)
        except AttributeError:
            raise ForbiddenError

    async def create_board(self, board_in, user, **extra_fields):
        board_db = await super().create(board_in, **extra_fields)
        await create_boards_user_relation(self.conn, board_db.uuid, user.uid)
        return self._interfaces_factory.create_output_model_object(board_db)

    async def update_board(self, board_in, user_available_boards, board_uuid):
        if board_uuid in user_available_boards:
            board_db = await super().update(board_in, filters={'uuid__exact': board_uuid}, excluded={'uuid'})
            return self._interfaces_factory.create_output_model_object(board_db)
        else:
            raise ForbiddenError

    async def delete_board(self, user_available_boards, board_uuid):
        if board_uuid in user_available_boards:
            board_db = await super().delete(uuid__exact=board_uuid)
            return self._interfaces_factory.create_output_model_object(board_db[0])
        else:
            raise ForbiddenError
