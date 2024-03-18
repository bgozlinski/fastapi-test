from datetime import timedelta

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..models import Todos, Users
from ..main import app
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URI = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'string', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture()
def test_todo():
    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday',
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()


@pytest.fixture()
def test_user():
    user = Users(
        username='string',
        email='string',
        first_name='string',
        last_name='string',
        hashed_password=bcrypt_context.hash('testpassword'),
        role='admin',
        phone_number='111111111'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()


@pytest.fixture()
def test_user_token():
    return {'username': 'testuser',
            'user_id': 1,
            'role': 'user',
            'expires_delta': timedelta(days=1)
            }
