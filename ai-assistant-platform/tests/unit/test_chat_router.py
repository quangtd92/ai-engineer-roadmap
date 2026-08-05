from fastapi.testclient import TestClient

from ai_assistant_platform.main import app

client = TestClient(app)


def test_chat_endpoint_success():
    response = client.post("/api/v1/chat", json={"content": "Hello World"})
    assert response.status_code == 200
    assert response.json() == {"reply": "Mock reply to: Hello World"}
