import sys
import os
import json
from typing import Any
from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from router.users_router import router
from db_config import get_db


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py



def start_application():
    app = FastAPI()
    app.include_router(router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./db/local_sqlite/test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    # Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    # Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client



def test_tc0001_get_all_users(client):
    td_first_record = 0
    td_username = 'darth.vader'
    td_email = 'darth.vader@gmail.com'
    td_role = 'villain'
    td_expected_record_count = 3
    td_id = 1 

    response = client.get("/users/v1")

    assert response.status_code == 200
    assert response.json()[td_first_record]['id'] == td_id
    assert response.json()[td_first_record]['username'] == td_username
    assert response.json()[td_first_record]['email'] == td_email
    assert response.json()[td_first_record]['role'] == td_role
    assert len(response.json()) == td_expected_record_count


def test_tc0002_get_by_username(client):
    td_username = 'darth.vader'
    td_email = 'darth.vader@gmail.com'
    td_role = 'villain'

    response = client.get(f'/users/v1/{td_username}')

    assert response.status_code == 200
    assert response.json()['username'] == td_username
    assert response.json()['email'] == td_email
    assert response.json()['role'] == td_role


def test_tc0003_invalid_username(client):
    td_username = 'invalid.username'

    response = client.get(f'/users/v1/{td_username}')

    assert response.status_code == 404
    assert response.json()['detail'] == 'username not found. Please check your parameter and try again.'


def tc_test_tc0004_post(client):
    td_username = 'test.username'
    td_email = 'test.username@gmail.com'
    td_role = 'test.role'

    response = client.post(f'/users/v1/', data = json.dumps(dict(
        username = td_username,
        email = td_email,
        role = td_role
    )))

    assert response.status_code == 201
    assert response.json() == td_username
    assert response.json() == td_email
    assert response.json() == td_role

    get_response = client.get(f'/users/v1/{td_username}')

    assert get_response.status_code == 200
    assert get_response.json() == td_username
    assert get_response.json() == td_email
    assert get_response.json() == td_role


def tc_test_tc0005_post_existing_username(client):
    td_username = 'darth.vader'
    td_email = 'test@gmail.com'
    td_role = 'test'
    td_message = 'username already exists. Please check your parameter and try again.'

    response = client.post(f'/users/v1/', data = json.dumps(dict(
        username = td_username,
        email = td_email,
        role = td_role
    )))

    assert response.status_code == 409
    assert response.json()['detail'] == td_message


def test_tc0006_exiting_email(client):
    td_username = 'test.username'
    td_email = 'darth.vader@gmail.com'
    td_role = 'test.role'
    td_message = 'email already exists. Please check your parameter and try again.'

    response = client.post(f'/users/v1/', data = json.dumps(dict(
        username = td_username,
        email = td_email,
        role = td_role
    )))

    assert response.status_code == 409
    assert response.json()['detail'] == td_message


def test_tc0007_post_empty_username(client):
    td_username = ''
    td_email = ''
    td_role = ''
    td_message = 'username cannot be empty. Please check your parameter and try again.'

    response = client.post(f'/users/v1/', data = json.dumps(dict(
        username = td_username,
        email = td_email,
        role = td_role
    )))

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0008_post_empty_email(client):
    td_username = 'test.username'
    td_email = ''
    td_role = ''
    td_message = 'email cannot be empty. Please check your parameter and try again.'

    response = client.post(f'/users/v1/', data = json.dumps(dict(
        username = td_username,
        email = td_email,
        role = td_role
    )))

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0009_post_empty_role(client):
    td_username = 'test.username'
    td_email = 'test.username@gmail.com'
    td_role = ''
    td_message = 'role cannot be empty. Please check your parameter and try again.'

    response = client.post(f'/users/v1/', data = json.dumps(dict(
        username = td_username,
        email = td_email,
        role = td_role
    )))

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0010_put(client):
    td_id = 1
    td_username = 'darth.vader'
    td_email = 'test@gmail.com'
    td_role = 'test'
    td_payload = '{"email": "test@gmail.com", "role": "test"}'

    response = client.put(f"/users/v1/{td_username}", data= td_payload, content= 'application/json')

    assert response.status_code == 204
    
    get_response = client.get(f'/users/v1/{td_username}')

    assert get_response.status_code == 200
    assert get_response.json()['id'] == td_id
    assert get_response.json()['username'] == td_username
    assert get_response.json()['email'] == td_email
    assert get_response.json()['role'] == td_role


def test_tc0011_put_update_email(client):
    td_username = 'darth.vader'
    td_email = 'test@gmail.com'
    td_role = 'villain'
    td_payload = '{"email": "test@gmail.com"}'


    response = client.put(f'/users/v1/{td_username}', data= td_payload, content= 'application/json')

    assert response.status_code == 204

    get_response = client.get(f'/users/v1/{td_username}')

    assert get_response.status_code == 200
    assert get_response.json()['username'] == td_username
    assert get_response.json()['email'] == td_email
    assert get_response.json()['role'] == td_role


def test_tc0012_put_update_role(client):
    td_username = 'darth.vader'
    td_email = 'darth.vader@gmail.com'
    td_role = 'hero'
    td_payload = '{"role": "hero"}'


    response = client.put(f'/users/v1/{td_username}', data= td_payload, content= 'application/json')

    assert response.status_code == 204

    get_response = client.get(f'/users/v1/{td_username}')

    assert get_response.status_code == 200
    assert get_response.json()['username'] == td_username
    assert get_response.json()['email'] == td_email
    assert get_response.json()['role'] == td_role


def test_tc0013_put_no_body(client):
    td_username = 'darth.vader'
    td_payload = '{}'
    td_message = 'request body cannot be empty. Please check your payload and try again'


    response = client.put(f'/users/v1/{td_username}', data= td_payload, content= 'application/json')

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0014_put_bad_username(client):
    td_username = 'this.is.bad'
    td_payload = '{"email": "test@gmail.com", "role": "test"}'
    td_message = 'username not found. Please check your username and try again.'

    response = client.put(f'/users/v1/{td_username}', data= td_payload, content= 'application/json')

    assert response.status_code == 404
    assert response.json()['detail'] == td_message


def test_tc0015_put_empty_fields(client):
    td_username = 'darth.vader'
    td_payload = '{"email": "", "role": ""}'
    td_message = 'request body fields cannot be empty. Please check your payload and try again'

    response = client.put(f'/users/v1/{td_username}', data= td_payload, content= 'application/json')

    assert response.status_code == 400
    assert response.json()['detail'] == td_message