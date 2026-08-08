import pytest
from fastapi.testclient import TestClient

from ai_assistant_platform.api.routes import chat as chat_route
from ai_assistant_platform.core.errors import InvalidMessageError
from ai_assistant_platform.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_chat_success(client: TestClient):
    response = client.post("/api/v1/chat", json={"content": "Hello there"})
    assert response.status_code == 200
    assert "reply" in response.json()


def test_chat_empty_content(client: TestClient):
    response = client.post("/api/v1/chat", json={"content": ""})
    assert response.status_code == 422


def test_chat_whitespace_content(client: TestClient):
    response = client.post("/api/v1/chat", json={"content": "   "})
    assert response.status_code == 422


def test_chat_content_too_long(client: TestClient):
    long_content = "a" * 1001
    response = client.post("/api/v1/chat", json={"content": long_content})
    assert response.status_code == 422


def test_chat_missing_content(client: TestClient):
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422


def test_chat_domain_error(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    def reject_message(_message):
        raise InvalidMessageError("Message was rejected by the chat service")

    monkeypatch.setattr(chat_route, "build_mock_reply", reject_message)

    response = client.post("/api/v1/chat", json={"content": "Hello there"})

    assert response.status_code == 400
    assert response.json() == {
        "code": "INVALID_MESSAGE",
        "detail": "Message was rejected by the chat service",
    }


def test_chat_openapi_documents_runtime_error_contract(client: TestClient):
    operation = client.get("/openapi.json").json()["paths"]["/api/v1/chat"]["post"]
    responses = operation["responses"]

    assert responses["400"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/ErrorResponse"
    )
    assert responses["422"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/ErrorResponse"
    )
