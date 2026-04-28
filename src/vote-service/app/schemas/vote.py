from typing import Literal
from pydantic import BaseModel, field_validator

class VoteRequest(BaseModel):
    salary_submission_id: int
    vote_type: Literal["UP", "DOWN"]

    @field_validator("vote_type", mode="before")
    @classmethod
    def normalize_vote_type(cls, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value

class ReportRequest(BaseModel):
    salary_submission_id: int
    reason: str
class ReportDelete(BaseModel):
    salary_submission_id: int
  

