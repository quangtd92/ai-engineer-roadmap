from pydantic import BaseModel, field_validator


class PredictionResponse(BaseModel):
    intent: str
    confidence: float
    model_version: str


class IntentPredictionRequest(BaseModel):
    text: str
    source: str = "web_ui"

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Text cannot be empty")
        return v
    