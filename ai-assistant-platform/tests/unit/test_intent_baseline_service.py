import pytest

from ai_assistant_platform.api.schemas.ml import PredictionResponse
from ai_assistant_platform.core.errors import NotFoundError
from ai_assistant_platform.services.intent_baseline_service import IntentBaselineService


def test_intent_baseline_service_schema():
    service = IntentBaselineService(
        artifact_path="models/sklearn_intent_baseline.joblib"
    )
    result = service.predict("thời tiết hôm nay")

    assert isinstance(result, PredictionResponse)
    assert isinstance(result.intent, str)
    assert len(result.intent) > 0
    assert 0.0 <= result.confidence <= 1.0
    assert result.model_version == "sklearn_intent_v1"


def test_intent_baseline_service_artifact_path_not_exist():
    with pytest.raises(NotFoundError, match="Model not found"):
        IntentBaselineService(artifact_path="models/non_exist.joblib")
