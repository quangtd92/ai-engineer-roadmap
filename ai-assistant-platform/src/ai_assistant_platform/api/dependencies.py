from functools import lru_cache

from ai_assistant_platform.core.config import Settings


@lru_cache
def get_settings():
    return Settings()
