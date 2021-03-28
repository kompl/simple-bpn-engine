from fastapi import APIRouter, Depends
from authorization.application_layer.interfaces import UserIn, UserOut, TokenOut
from authorization.application_layer.services.auth_services import AuthService
from server_configs.setup import db_pool
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(
    prefix="/api/boards",
    tags=["Auth"],
    responses={404: {"description": "Not found"},
               204: {"description": "Does not exists"}},
)


async def build_auth_service():
    pool = await db_pool
    service = AuthService()
    service.setup(pool)
    return service

