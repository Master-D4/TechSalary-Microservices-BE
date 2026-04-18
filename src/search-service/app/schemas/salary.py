from datetime import datetime
from decimal import Decimal
from typing import Literal
from typing import List

from pydantic import BaseModel

Status = Literal["PENDING", "APPROVED", "REJECTED"]

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

class SalaryListResponse(BaseModel):
    items: List[SalaryResponse]
    total: int
    page: int
    limit: int