from typing import Any
from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from router.users_router import router
from db_config import get_db
import sys
import os
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


    # Tests that function raises HTTPException when username does not exist in database
    def test_tc0003_invalid_username(client):
        td_username = 'invalid.username'

        response = client.get(f'/users/v1/{td_username}')

        assert response.status_code == 404
        assert response.json()['detail'] == 'username not found. Please check your parameter and try again.'