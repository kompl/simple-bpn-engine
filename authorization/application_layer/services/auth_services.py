from authorization.application_layer.interfaces import UserIn, TokenOut
from fastapi_async_db_utils import create, read_by_params
from datetime import timedelta
from authorization.application_layer.services.interfaces_factories import UserInterfacesFactory
from authorization.infrastructure_layer.utils import get_timestamp
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from authorization.infrastructure_layer.exceptions import UnauthorizedError, ForbiddenError, DoesNotExistError
from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from server_configs.setup import SECRET_KEY


class AuthService:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 300
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.conn = None
        self._interface_fabric = UserInterfacesFactory()

    def setup(self, db_pool):
        self.conn = db_pool

    async def create_user(self, user_in: UserIn):
        user_db = self._interface_fabric.create_db_model_object(user_name=user_in.user_name,
                                                                hashed_password=self.get_password_hash(
                                                                    user_in.password),
                                                                disabled=False)
        try:
            return await create(self.conn, user_db)
        except UniqueViolationError:
            raise HTTPException(status_code=400, detail="this username already exist")

    async def create_access_token(self, form_data: OAuth2PasswordRequestForm):

        verified_user = await self.authenticate_user(form_data.username, form_data.password)
        access_token = self._create_access_token(verified_user)
        return TokenOut(**{"access_token": access_token, "token_type": "bearer"})

    def _create_access_token(self, user_db):
        user_data = {"sub": user_db.user_name,
                     "exp": get_timestamp() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
                     }
        encoded_jwt = jwt.encode(user_data, SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise ForbiddenError
            current_user = await self._get_user_by_username(username)
            return current_user
        except JWTError:
            raise ForbiddenError
        except DoesNotExistError:
            raise ForbiddenError

    async def authenticate_user(self, username, password):
        current_user = await self._get_user_by_username(username)
        if not self.verify_password(password, current_user.hashed_password):
            raise UnauthorizedError
        if current_user.disabled:
            raise ForbiddenError
        return current_user

    async def _get_user_by_username(self, username):
        user_db_model = self._interface_fabric.create_db_model_object(user_name=username)
        found_users = await read_by_params(self.conn, user_db_model, user_name=user_db_model.user_name)
        return found_users[0]

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
