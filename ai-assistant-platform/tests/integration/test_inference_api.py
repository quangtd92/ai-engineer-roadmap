import pytest
from fastapi.testclient import TestClient

from ai_assistant_platform.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_inference_success(client: TestClient):
    response = client.post("/api/v1/inference/score", json={"values": [1.0, 2.0]})
    assert response.status_code == 200
    data = response.json()
    score = data["score"]
    assert isinstance(score, float)


def test_inference_fail_length(client: TestClient):
    response = client.post("/api/v1/inference/score", json={"values": [1.0, 2.0, 3.0]})
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_inference_fail_nan(client: TestClient):
    response = client.post("/api/v1/inference/score", json={"values": [1.0, "nan"]})
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_inference_fail_missing(client: TestClient):
    response = client.post("/api/v1/inference/score", json={"values": []})
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"
