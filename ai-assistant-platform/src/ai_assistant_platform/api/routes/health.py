from ai_assistant_platform.core.config import Settings
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    settings = Settings()
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "app_env": settings.app_env,
    }

