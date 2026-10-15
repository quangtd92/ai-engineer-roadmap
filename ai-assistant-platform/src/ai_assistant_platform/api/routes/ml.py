from typing import Annotated

from fastapi import APIRouter, Depends

from ai_assistant_platform.api.dependencies import get_intent_service
from ai_assistant_platform.api.schemas.ml import (
    IntentPredictionRequest,
    PredictionResponse,
)
from ai_assistant_platform.services.intent_service import IntentService

router = APIRouter(prefix="/api/v1/ml", tags=["ml"])

@router.post(
    "/intent",
    response_model=PredictionResponse
)
def predict_intent(request: IntentPredictionRequest,
    service: Annotated[IntentService, Depends(get_intent_service)]
) -> PredictionResponse:
    """
    Dự đoán intent từ văn bản đầu vào.
    """
    return service.predict(text=request.text, source=request.source)