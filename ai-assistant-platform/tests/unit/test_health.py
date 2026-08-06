from fastapi.testclient import TestClient

from ai_assistant_platform.api.dependencies import get_settings
from ai_assistant_platform.core.config import Settings
from ai_assistant_platform.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "app_env" in data


def test_health_endpoint_with_dependency_override():
    mock_settings = Settings(app_name="test-app", app_env="testing")
    app.dependency_overrides[get_settings] = lambda: mock_settings

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["app_env"] == "testing"

    app.dependency_overrides.clear()
