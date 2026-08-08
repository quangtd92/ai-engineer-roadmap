"""Tests for the async status endpoint (Day 15)."""

from fastapi.testclient import TestClient

from ai_assistant_platform.main import app

client = TestClient(app)


class TestStatusEndpoint:
    """Test GET /api/v1/status endpoint."""

    def test_status_returns_200(self):
        """Route trả status code 200."""
        response = client.get("/api/v1/status")
        assert response.status_code == 200

    def test_status_returns_ready(self):
        """Response body là {"status": "ready"}."""
        response = client.get("/api/v1/status")
        data = response.json()
        assert data == {"status": "ready"}

    def test_status_called_multiple_times(self):
        """Gọi route nhiều lần đều trả kết quả nhất quán (không blocking)."""
        for _ in range(5):
            response = client.get("/api/v1/status")
            assert response.status_code == 200
            assert response.json()["status"] == "ready"
