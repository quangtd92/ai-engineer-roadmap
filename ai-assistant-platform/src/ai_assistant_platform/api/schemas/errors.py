from pydantic import BaseModel


class ValidationIssue(BaseModel):
    loc: list[str | int]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    code: str
    detail: str | list[ValidationIssue]
