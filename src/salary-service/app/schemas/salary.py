from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Literal

Status = Literal["PENDING", "APPROVED", "REJECTED"]

class SalaryCreate(BaseModel):
    job_title: str
    company: str
    location: str
    salary_amount: Decimal = Field(..., gt=0)
    currency: str = "LKR"
    years_experience: int = Field(..., ge=0)
    is_anonymous: bool = False

class SalaryResponse(BaseModel):
    id: int
    job_title: str
    company: str
    location: str
    salary_amount: Decimal
    currency: str
    years_experience: int
    status: Status
    is_anonymous: bool
    created_at: datetime

    class Config:
        from_attributes = True
