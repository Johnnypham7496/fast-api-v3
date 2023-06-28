from fastapi.testclient import TestClient
from main import app


client = TestClient(app)



def test_tc_0001_welcome():
    td_message = {"message": 'Hello, welcome to the Justice League\'s FastAPI'}

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == td_message