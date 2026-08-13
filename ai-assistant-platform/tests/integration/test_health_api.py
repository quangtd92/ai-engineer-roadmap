import pytest
from fastapi.testclient import TestClient

from ai_assistant_platform.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_success(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "app_env" in data
    assert "X-Request-ID" in response.headers


def test_status_success(client: TestClient):
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
    assert "X-Request-ID" in response.headers
