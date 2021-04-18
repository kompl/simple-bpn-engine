from pytest import mark
from httpx import Response
from server_configs.setup import SECRET_KEY
from jose import jwt
from zoneinfo import ZoneInfo
import os
import datetime


@mark.usefixtures('postgresql_instance')
class BaseTestCaseAuthView:
    MAX_RESPONSE_TIME_MCS = 1000000


class TestCaseCreateUserView(BaseTestCaseAuthView):

    @mark.asyncio
    async def test_create_user_with_available_username(self,
                                                       create_user_response_successful: Response,
                                                       user_name,
                                                       client
                                                       ):
        assert create_user_response_successful.status_code == 201
        assert create_user_response_successful.json() == {'userName': user_name, 'disabled': False,
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

    @mark.asyncio
    async def test_get_token_with_right_credentials(self,
                                                    get_token_response,
                                                    user_name,
                                                    user_password,
                                                    client):
        response: Response = await get_token_response(name=user_name, password=user_password)
        successful_response: dict = response.json()
        user_info = jwt.decode(successful_response['access_token'], self.SECRET_KEY, algorithms=[self.ALGORITHM])

        now_timestamp = datetime.datetime.now(tz=ZoneInfo(os.getenv('TZ'))).timestamp()
        expire_timestamp = now_timestamp + datetime.timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES).seconds

        assert response.status_code == 201
        assert response.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS
        assert user_info['sub'] == user_name
        assert user_info['exp'] <= expire_timestamp
        assert user_info['exp'] > now_timestamp

    @mark.asyncio
    async def test_get_token_with_wrong_password(self,
                                                 get_token_response,
                                                 user_name,
                                                 user_password,
                                                 client):
        wrong_password = 'wrong' + user_password
        response: Response = await get_token_response(name=user_name, password=wrong_password)
        assert response.status_code == 401
        assert response.json() == {'detail': 'incorrect credentials'}
        assert response.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS

    @mark.asyncio
    async def test_get_token_with_wrong_username(self,
                                                 get_token_response,
                                                 user_name,
                                                 user_password,
                                                 client):
        wrong_username = 'wrong' + user_name
        response: Response = await get_token_response(name=wrong_username, password=user_password)
        assert response.status_code == 401
        assert response.json() == {'detail': 'incorrect credentials'}
        assert response.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS


class TestCaseGetUserInfoView(BaseTestCaseAuthView):

    @mark.asyncio
    async def test_get_user_with_right_token(self,
                                             get_user_response,
                                             user_name,
                                             token,
                                             client):
        response: Response = await get_user_response(token)
        assert response.status_code == 200
        assert response.json() == {
            "userName": user_name,
            "disabled": False,
            "availableBoards": []
        }
        assert response.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS

    @mark.asyncio
    async def test_get_user_with_wrong_token(self,
                                             get_user_response,
                                             user_name,
                                             token,
                                             client):
        wrong_token = token[::-1]
        response: Response = await get_user_response(wrong_token)
        assert response.status_code == 403
        assert response.json() == {'detail': 'incorrect bearer token'}
        assert response.elapsed.microseconds < self.MAX_RESPONSE_TIME_MCS
