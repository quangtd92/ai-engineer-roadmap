import math

from pydantic import BaseModel, Field, field_validator


class InferenceRequest(BaseModel):
    values: list[float] = Field(
        ..., min_length=2, max_length=2, description="Input vector of 2 float values"
    )

    @field_validator("values")
    @classmethod
    def validate_content(cls, v: list[float]) -> list[float]:
        for val in v:
            if math.isnan(val) or math.isinf(val):
                raise ValueError("Value have to be a float")
        return v


class InferenceResponse(BaseModel):
    score: float
