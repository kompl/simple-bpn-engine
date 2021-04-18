from httpx import AsyncClient
from server_configs.asgi import app
from pytest import fixture


@fixture(scope="package", params=["test2"])
def user_name(request):
    return request.param


@fixture(scope="package", params=["test_password2"])
def user_password(request):
    return request.param


@fixture
def user_in(user_name, user_password):
    return {'userName': user_name, 'password': user_password}


@fixture
async def client():
    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000') as client:
        yield client


@fixture
async def create_user_response_successful(client, user_in):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    return await client.post('/api/auth/registration', json=user_in, headers=headers)


@fixture
async def create_user_response_failed(client, user_in, create_user_response_successful):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    return await client.post('/api/auth/registration', json=user_in, headers=headers)


@fixture
def get_token_response(create_user_response_successful, client):
    async def _get_token_response(name, password):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = f'grant_type=&username={name}&password={password}'
        return await client.post('/api/auth/token', data=data, headers=headers)
    return _get_token_response


@fixture
async def token(create_user_response_successful, client, user_name, user_password):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f'grant_type=&username={user_name}&password={user_password}'
    response = await client.post('/api/auth/token', data=data, headers=headers)
    serialized_response = response.json()
    return serialized_response['access_token']


@fixture
def get_user_response(token: str, client):
    async def _get_user_response(_token):
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + _token
        }
        return await client.get('/api/auth/users/me/', headers=headers)
    return _get_user_response
