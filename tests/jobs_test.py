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
from router.jobs_router import router
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



def test_tc0001_get_all_jobs(client):
    td_first_record = 0
    td_id = 1
    td_title = 'villain'
    td_company = 'sith'
    td_location = 'death star'
    td_description = 'looking to control the republic'

    response = client.get('/jobs/v1/')

    assert response.status_code == 200
    assert response.json()[td_first_record]['id'] == td_id
    assert response.json()[td_first_record]['title'] == td_title
    assert response.json()[td_first_record]['company'] == td_company
    assert response.json()[td_first_record]['location'] == td_location
    assert response.json()[td_first_record]['description'] == td_description


def test_tc0002_get_by_id(client):
    td_company = 'sith'
    td_title = 'villain'
    td_location = 'death star'
    td_description = 'looking to control the republic'
    td_id = 1

    response = client.get(f'/jobs/v1/{td_id}')

    assert response.status_code == 200
    assert response.json()['id'] == td_id
    assert response.json()['title'] == td_title
    assert response.json()['company'] == td_company
    assert response.json()['location'] == td_location
    assert response.json()['description'] == td_description


def test_tc0003_invalid_id(client):
    td_id = '0'
    td_message = f'company information with id {td_id} not found. Please check the ID number and try again.'

    response = client.get(f'/jobs/v1/{td_id}')

    assert response.status_code == 404
    assert response.json()['detail'] == td_message


def test_tc0004_post_job(client):
    td_username_request = 'darth.vader'
    td_title = 'villain'
    td_company = 'sith'
    td_location = 'death star'
    td_description = 'looking to control the republic'
    td_id = 4

    response = client.post('/jobs/v1/', data= json.dumps(dict(
        username=td_username_request,
        title=td_title,
        company=td_company,
        location=td_location,
        description=td_description
    )))

    assert response.status_code == 201  
    assert response.json()['id'] == td_id
    assert response.json()['title'] == td_title
    assert response.json()['company'] == td_company
    assert response.json()['location'] == td_location
    assert response.json()['description'] == td_description


def test_tc0005_post_username_not_found(client):
    td_username = 'test_username'
    td_title = 'test_title'
    td_company = 'test_company'
    td_location = 'test_location'
    td_description = 'test_description'
    td_message = 'username not found. Please check your parameter and try again.'

    response = client.post('/jobs/v1/', data= json.dumps(dict(
        username=td_username,
        title=td_title,
        company=td_company,
        location=td_location,
        description=td_description
    )))

    assert response.status_code == 404
    assert response.json()['detail'] == td_message


def test_tc0006_post_empty_title(client):
    td_username = 'darth.vader'
    td_title = ''
    td_company = ''
    td_location = ''
    td_description = ''
    td_message = 'title field cannot be empty. Please check your parameter and try again.'

    response = client.post('/jobs/v1/', data= json.dumps(dict(
        username=td_username,
        title=td_title,
        company=td_company,
        location=td_location,
        description=td_description
    )))

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0007_post_empty_company(client):
    td_username = 'darth.vader'
    td_title = 'test_title'
    td_company = ''
    td_location = ''
    td_description = ''
    td_message = 'company field cannot be empty. Please check your parameter and try again.'

    response = client.post('/jobs/v1/', data= json.dumps(dict(
        username=td_username,
        title=td_title,
        company=td_company,
        location=td_location,
        description=td_description
    )))

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0008_post_empty_location(client):
    td_username = 'darth.vader'
    td_title = 'test_title'
    td_company = 'test_company'
    td_location = ''
    td_description = ''
    td_message = 'location field cannot be empty. Please check your parameter and try again.'

    response = client.post('/jobs/v1/', data= json.dumps(dict(
        username=td_username,
        title=td_title,
        company=td_company,
        location=td_location,
        description=td_description
    )))

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0009_post_empty_description(client):
    td_username = 'darth.vader'
    td_title = 'test_title'
    td_company = 'test_company'
    td_location = 'test_location'
    td_description = ''
    td_message = 'description field cannot be empty. Please check your parameter and try again.'

    response = client.post('/jobs/v1/', data= json.dumps(dict(
        username=td_username,
        title=td_title,
        company=td_company,
        location=td_location,
        description=td_description
    )))

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0010_put(client):
    td_id = 1
    td_title = 'test title'
    td_company = 'test company'
    td_location = 'test location'
    td_description = 'test description'
    td_headers = 'Successfully updated job details'
    td_payload = '{"title": "test title", "company": "test company", "location": "test location", "description": "test description"}'

    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content= 'application/json')

    assert response.status_code == 204
    assert response.headers['message'] == td_headers

    get_response = client.get(f'/jobs/v1/{td_id}')
    
    assert get_response.status_code == 200
    assert get_response.json()['title'] == td_title
    assert get_response.json()['company'] == td_company
    assert get_response.json()['location'] == td_location
    assert get_response.json()['description'] == td_description


def test_tc0011_put_title(client):
    td_id = 1
    td_title = 'test title'
    td_headers = 'Successfully updated job details'
    td_payload = '{"title": "test title", "company": "", "location": "", "description": ""}'

    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content= 'application/json')

    assert response.status_code == 204
    assert response.headers['message'] == td_headers

    get_response = client.get(f'/jobs/v1/{td_id}')
    
    assert get_response.status_code == 200
    assert get_response.json()['title'] == td_title


def test_tc0012_put_company(client):
    td_id = 1
    td_company = 'test company'
    td_headers = 'Successfully updated job details'
    td_payload = '{"title": "", "company": "test company", "location": "", "description": ""}'

    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content= 'application/json')

    assert response.status_code == 204
    assert response.headers['message'] == td_headers

    get_response = client.get(f'/jobs/v1/{td_id}')
    
    assert get_response.status_code == 200
    assert get_response.json()['company'] == td_company


def test_tc0012_put_location(client):
    td_id = 1
    td_location = 'test location'
    td_headers = 'Successfully updated job details'
    td_payload = '{"title": "", "company": "", "location": "test location", "description": ""}'

    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content= 'application/json')

    assert response.status_code == 204
    assert response.headers['message'] == td_headers

    get_response = client.get(f'/jobs/v1/{td_id}')
    
    assert get_response.status_code == 200
    assert get_response.json()['location'] == td_location


def test_tc0012_put_description(client):
    td_id = 1
    td_description = 'test description'
    td_headers = 'Successfully updated job details'
    td_payload = '{"title": "", "company": "", "location": "", "description": "test description"}'

    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content= 'application/json')

    assert response.status_code == 204
    assert response.headers['message'] == td_headers

    get_response = client.get(f'/jobs/v1/{td_id}')
    
    assert get_response.status_code == 200
    assert get_response.json()['description'] == td_description


def test_tc0013_put_no_body(client):
    td_id = 1
    td_message = 'request body fields cannot be empty. Please check your payload and try again.'
    td_payload = '{"title": "", "company": "", "location": "", "description": ""}'

    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content= 'application/json')

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_tc0013_put_empty_fields(client):
    td_id = 1
    td_message = 'request body fields cannot be empty. Please check your payload and try again.'
    td_payload = '{"title": "", "company": "", "location": "", "description": ""}'

    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content= 'application/json')

    assert response.status_code == 400
    assert response.json()['detail'] == td_message


def test_0014_put_invalid_id(client):
    td_id = 1234
    td_message = f'ID number {td_id} does not exist. Please check your parameter and try again.'
    td_payload = '{"title": "test title", "company": "test company", "location": "test location", "description": "test description"}'


    response = client.put(f'/jobs/v1/{td_id}', data= td_payload, content='application/json')

    assert response.status_code == 404
    assert response.json()['detail'] == td_message