from fastapi import status
from .utils import *
from ..routers.auth import get_db, authenticated_user, create_access_token, get_current_user, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db


def test_authenticated_user(test_user):
    db = TestingSessionLocal()

    authenticate_user = authenticated_user(test_user.username, 'testpassword', db)
    assert authenticate_user is not None
    assert authenticate_user.username == test_user.username

    non_existent_user = authenticated_user('Wrong username', 'testpassword', db)
    assert non_existent_user is False

    wrong_password_user = authenticated_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False


def test_create_access_token(test_user_token):
    token = create_access_token(username=test_user_token['username'],
                                user_id=test_user_token['user_id'],
                                role=test_user_token['role'],
                                expires_delta=test_user_token['expires_delta']
                                )

    decoded_token = jwt.decode(token,
                               SECRET_KEY,
                               algorithms=[ALGORITHM],
                               options={"verify_signature": False}
                               )

    assert decoded_token['sub'] == test_user_token['username']
    assert decoded_token['id'] == test_user_token['user_id']
    assert decoded_token['role'] == test_user_token['role']


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': encode['sub'], 'id': encode['id'], 'user_role': encode['role']}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'
