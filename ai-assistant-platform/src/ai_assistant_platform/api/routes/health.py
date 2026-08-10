import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from ai_assistant_platform.api.dependencies import get_settings
from ai_assistant_platform.api.schemas.health import HealthResponse
from ai_assistant_platform.core.config import Settings

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
def health_check(settings: Annotated[Settings, Depends(get_settings)]):
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        app_env=settings.app_env,
    )
