from pydantic import BaseModel


class PredictionResponse(BaseModel):
    intent: str
    confidence: float
    model_version: str
