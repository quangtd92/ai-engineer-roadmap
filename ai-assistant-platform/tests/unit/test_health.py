from ai_assistant_platform.api.routes.health import health_check
from ai_assistant_platform.api.schemas.health import HealthResponse
from ai_assistant_platform.core.config import Settings


def test_health_check():
    """Unit test: gọi trực tiếp hàm health_check không qua HTTP/TestClient."""
    settings = Settings(app_name="unit-test-app", app_env="testing")
    response = health_check(settings=settings)

    assert isinstance(response, HealthResponse)
    assert response.status == "ok"
    assert response.app_name == "unit-test-app"
    assert response.app_env == "testing"
