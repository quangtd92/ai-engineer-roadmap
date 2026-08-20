from typing import Annotated

from fastapi import APIRouter, Depends

from ai_assistant_platform.api.dependencies import get_inference_service
from ai_assistant_platform.api.schemas.inference import (
    InferenceRequest,
    InferenceResponse,
)
from ai_assistant_platform.services.inference_service import InferenceService

router = APIRouter(prefix="/api/v1", tags=["inference"])


@router.post("/inference/score")
def post_score(
    data: InferenceRequest,
    service: Annotated[InferenceService, Depends(get_inference_service)],
) -> InferenceResponse:
    result = service.run_inference(data.values)
    return InferenceResponse(score=result)
