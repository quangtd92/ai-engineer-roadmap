from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    content: str = Field(
        ..., 
        min_length=1,
        max_length=1000,
        description="Message content"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Content cannot be empty")
        return v

class ChatResponse(BaseModel):
    reply: str