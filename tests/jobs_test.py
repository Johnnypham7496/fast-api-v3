from typing import Any
from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from router.jobs_router import router
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



def test_tc0001_get_all_jobs(client):
    td_first_record = 0
    td_id = 1
    td_title = 'villain'
    td_company = 'sith'
    td_location = 'death star'
    td_description = 'looking to control the republic'

    response = client.get('/jobs/v1')

    assert response.status_code == 200
    assert response.json()[td_first_record]['id'] == td_id
    assert response.json()[td_first_record]['title'] == td_title
    assert response.json()[td_first_record]['company'] == td_company
    assert response.json()[td_first_record]['location'] == td_location
    assert response.json()[td_first_record]['description'] == td_description


def test_tc0002_get_by_company(client):
    td_company = 'sith'
    td_title = 'villain'
    td_location = 'death star'
    td_description = 'looking to control the republic'
    td_id = 1

    response = client.get(f'/jobs/v1/{td_company}')

    assert response.status_code == 200
    assert response.json()['id'] == td_id
    assert response.json()['title'] == td_title
    assert response.json()['company'] == td_company
    assert response.json()['location'] == td_location
    assert response.json()['description'] == td_description


def test_tc0003_invalid_company(client):
    td_company = 'invalid company'
    td_message = 'company information not found. Please check your parameter and try again.'

    response = client.get(f'/jobs/v1/{td_company}')

    assert response.status_code == 404
    assert response.json()['detail'] == td_message