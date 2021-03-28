from fastapi import APIRouter, Depends
from authorization.application_layer.interfaces import UserIn, UserOut, TokenOut
from authorization.application_layer.services.auth_services import AuthService
from server_configs.setup import db_pool
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"},
               204: {"description": "Does not exists"}},
)


async def build_auth_service():
    pool = await db_pool
    service = AuthService()
    service.setup(pool)
    return service


@auth_router.post(
    "/registration",
    description='User Registration',
    response_model=UserOut,
    status_code=201
)
async def create_user(user_in: UserIn, service: AuthService = Depends(build_auth_service)):
    return await service.create_user(user_in)


@auth_router.post(
    "/token",
    description='Get Token',
    response_model=TokenOut,
    status_code=201
)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           service: AuthService = Depends(build_auth_service)):
    return await service.create_access_token(form_data)


@auth_router.get("/users/me/", response_model=UserOut)
async def read_me(token: str = Depends(AuthService.oauth2_scheme), service: AuthService = Depends(build_auth_service)):
    return await service.get_current_user(token)
