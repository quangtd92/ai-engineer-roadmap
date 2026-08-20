import pytest
from pydantic import ValidationError

from ai_assistant_platform.api.schemas.inference import InferenceRequest
from ai_assistant_platform.services.inference_service import InferenceService


def test_run_inference_deterministic():
    service1 = InferenceService()
    service2 = InferenceService()

    result1 = service1.run_inference([1.0, 2.0])
    result2 = service2.run_inference([1.0, 2.0])

    assert result1 == result2


def test_run_inference_type_data_check():
    inference_service = InferenceService()
    result = inference_service.run_inference([1.0, 2.0])
    assert isinstance(result, float)


def test_inference_request_invalid_length():
    with pytest.raises(ValidationError):
        InferenceRequest(values=[1.0])

    with pytest.raises(ValidationError):
        InferenceRequest(values=[1.0, 2.0, 3.0])


def test_inference_request_invalid_values():
    with pytest.raises(ValidationError):
        InferenceRequest(values=[float("nan"), 1.0])

    with pytest.raises(ValidationError):
        InferenceRequest(values=[float("inf"), 1.0])
