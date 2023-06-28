from fastapi.testclient import TestClient
from main import app


client = TestClient(app)



def test_tc_0001_welcome():
    td_message = {"message": 'Hello, welcome to the Justice League\'s FastAPI'}

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == td_message


def test_tc0002_health():
    td_messgae = {'status': 'OK'}

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == td_messgae