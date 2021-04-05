from fastapi import APIRouter, Depends, Query
from authorization.application_layer.auth_routing import get_user, UserOut
from core.application_layer.services.managers import BoardService
from server_configs.setup import db_pool
from core.application_layer.output_models import BoardOut
from typing import Optional, List

boards_router = APIRouter(
    prefix="/api/boards",
    tags=["Boards"],
    responses={404: {"description": "Not found"},
               204: {"description": "Does not exists"}},
)


async def build_board_service():
    pool = await db_pool
    service = BoardService()
    service.setup(pool)
    return service


# noinspection PyPep8Naming
@boards_router.get(
    "/",
    description='Get Available Boards',
    response_model=BoardOut,
    status_code=200
)
async def get_boards(user: UserOut = Depends(get_user),
                     service: BoardService = Depends(build_board_service),
                     name: Optional[str] = Query('', max_length=50),
                     description: Optional[str] = Query('', max_length=50),
                     orderBy: Optional[List] = Query(['name'], description='Поля на схеме BoardOut'),
                     pageSize: Optional[int] = Query(10),
                     pageNumber: Optional[int] = Query(1)
                     ):
    return await service.read_list(orderBy,
                                   pageSize,
                                   pageNumber,
                                   boards=('uuid', {'name__contains': name,
                                                    'description__iexact': description}),
                                   users=('uid', {'uid__exact': user.uid})
                                   )
