from pytest import fixture, mark
from httpx import AsyncClient, Response
from server_configs.asgi import app
from server_configs.setup import SECRET_KEY
from jose import jwt
from zoneinfo import ZoneInfo
import os
import datetime


class BaseTestCaseAuthView:
    user_name = 'test'
    user_password = 'test'
    MAX_RESPONSE_TIME_MCS = 1000000

    @fixture
    def user_in(self):
        return {'userName': self.user_name, 'password': self.user_password}

    @fixture
    async def client(self):
        async with AsyncClient(app=app, base_url='http://0.0.0.0:8000') as client:
            yield client

    @fixture
    async def create_user_response_successful(self, client, user_in):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        return await client.post('/api/auth/registration', json=user_in, headers=headers)


class TestCaseCreateUserView(BaseTestCaseAuthView):

    @fixture
    async def create_user_response_failed(self, client, user_in, create_user_response_successful):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        return await client.post('/api/auth/registration', json=user_in, headers=headers)

    @mark.asyncio
    async def test_create_user_with_available_username(self,
                                                       create_user_response_successful: Response,
                                                       client
                                                       ):
        assert create_user_response_successful.status_code == 201
        assert create_user_response_successful.json() == {'userName': self.user_name, 'disabled': False,
                                                          'availableBoards': []}
        assert create_user_response_successful.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS

    @mark.asyncio
    async def test_create_user_with_pre_existing_username(self,
                                                          create_user_response_failed: Response,
                                                          client
                                                          ):
        assert create_user_response_failed.status_code == 400
        assert create_user_response_failed.json() == {'detail': 'this username already exist'}
        assert create_user_response_failed.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS


class TestCaseGetTokenView(BaseTestCaseAuthView):
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 300
    SECRET_KEY = SECRET_KEY

    @fixture
    async def get_token_response_with_right_credentials(self, create_user_response_successful, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = f'grant_type=&username={self.user_name}&password={self.user_password}'
        return await client.post('/api/auth/token', data=data, headers=headers)

    @fixture
    async def get_token_response_with_wrong_username(self, create_user_response_successful, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = f'grant_type=&username=wrong_username&password={self.user_password}'
        return await client.post('/api/auth/token', data=data, headers=headers)

    @fixture
    async def get_token_response_with_wrong_password(self, create_user_response_successful, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = f'grant_type=&username={self.user_name}&password=wrong_password'
        return await client.post('/api/auth/token', data=data, headers=headers)

    @mark.asyncio
    async def test_get_token_with_right_credentials(self,
                                                    get_token_response_with_right_credentials: Response,
                                                    client):
        successful_response: dict = get_token_response_with_right_credentials.json()
        user_info = jwt.decode(successful_response['access_token'], self.SECRET_KEY, algorithms=[self.ALGORITHM])

        now_timestamp = datetime.datetime.now(tz=ZoneInfo(os.getenv('TZ'))).timestamp()
        expire_timestamp = now_timestamp + datetime.timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES).seconds

        assert get_token_response_with_right_credentials.status_code == 201
        assert get_token_response_with_right_credentials.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS
        assert user_info['sub'] == self.user_name
        assert user_info['exp'] <= expire_timestamp
        assert user_info['exp'] > now_timestamp

    @mark.asyncio
    async def test_get_token_with_wrong_password(self,
                                                 get_token_response_with_wrong_password: Response,
                                                 client):
        assert get_token_response_with_wrong_password.status_code == 401
        assert get_token_response_with_wrong_password.json() == {'detail': 'incorrect credentials'}
        assert get_token_response_with_wrong_password.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS

    @mark.asyncio
    async def test_get_token_with_wrong_username(self,
                                                 get_token_response_with_wrong_username: Response,
                                                 client):
        assert get_token_response_with_wrong_username.status_code == 401
        assert get_token_response_with_wrong_username.json() == {'detail': 'incorrect credentials'}
        assert get_token_response_with_wrong_username.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS


class TestCaseGetUserInfoView(BaseTestCaseAuthView):

    @fixture
    async def token(self, create_user_response_successful, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = f'grant_type=&username={self.user_name}&password={self.user_password}'
        response = await client.post('/api/auth/token', data=data, headers=headers)
        serialized_response = response.json()
        return serialized_response['access_token']

    @fixture
    async def get_user_response_with_right_token(self, token: str, client):
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        return await client.get('/api/auth/users/me/', headers=headers)

    @fixture
    async def get_user_response_with_wrong_token(self, client):
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer wrong_token'
        }
        return await client.get('/api/auth/users/me/', headers=headers)

    @mark.asyncio
    async def test_get_user_with_right_token(self,
                                             get_user_response_with_right_token: Response,
                                             client):
        assert get_user_response_with_right_token.status_code == 200
        assert get_user_response_with_right_token.json() == {
            "userName": self.user_name,
            "disabled": False,
            "availableBoards": []
        }
        assert get_user_response_with_right_token.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS

    @mark.asyncio
    async def test_get_user_with_wrong_token(self,
                                             get_user_response_with_wrong_token: Response,
                                             client):
        assert get_user_response_with_wrong_token.status_code == 403
        assert get_user_response_with_wrong_token.json() == {'detail': 'incorrect bearer token'}
        assert get_user_response_with_wrong_token.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS
