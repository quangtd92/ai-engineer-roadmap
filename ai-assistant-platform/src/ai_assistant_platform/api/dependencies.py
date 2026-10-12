from functools import lru_cache

from ai_assistant_platform.core.config import Settings
from ai_assistant_platform.services.inference_service import InferenceService


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_inference_service():
    return InferenceService()

from ai_assistant_platform.services.intent_service import IntentService


@lru_cache
def get_intent_service() -> IntentService:
    return IntentService(
        classifier_path="models/intent_classifier.pt",
        metadata_path="models/intent_metadata.json",
        preprocessor_path="models/intent_preprocessor.joblib",
    )
