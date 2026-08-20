from functools import lru_cache

from ai_assistant_platform.core.config import Settings
from ai_assistant_platform.services.inference_service import InferenceService


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_inference_service():
    return InferenceService()
