import pytest
from fastapi.testclient import TestClient

from ai_assistant_platform.api.dependencies import get_intent_service
from ai_assistant_platform.core.errors import NotFoundError
from ai_assistant_platform.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_predict_intent_success(client: TestClient):
    response = client.post(
        "/api/v1/ml/intent",
        json={"text": "lên lịch họp dự án chiều nay"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["intent"], str)
    assert len(data["intent"]) > 0
    assert isinstance(data["confidence"], float)
    assert 0.0 <= data["confidence"] <= 1.0
    assert data["model_version"] == "torch_intent_v1"


def test_predict_intent_with_custom_source(client: TestClient):
    response = client.post(
        "/api/v1/ml/intent",
        json={"text": "tìm tài liệu dự án", "source": "phone"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["intent"], str)
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_intent_validation_empty_text(client: TestClient):
    response = client.post(
        "/api/v1/ml/intent",
        json={"text": "   "},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "VALIDATION_ERROR"


def test_predict_intent_validation_missing_text(client: TestClient):
    response = client.post(
        "/api/v1/ml/intent",
        json={},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "VALIDATION_ERROR"


def test_predict_intent_artifact_not_found(client: TestClient):
    def mock_get_intent_service():
        raise NotFoundError("Model artifact not found at models/non_existent.pt")

    app.dependency_overrides[get_intent_service] = mock_get_intent_service

    try:
        response = client.post(
            "/api/v1/ml/intent",
            json={"text": "kiểm tra model không tồn tại"},
        )
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "NOT_FOUND_ERROR"
    finally:
        app.dependency_overrides.clear()
