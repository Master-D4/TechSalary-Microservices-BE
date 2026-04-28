from pydantic import BaseModel, condecimal, constr, conint
from datetime import datetime

NonEmptyStr = constr(strip_whitespace=True, min_length=1)


class SalaryCreate(BaseModel):
    job_title: NonEmptyStr
    company: NonEmptyStr
    location: NonEmptyStr

    salary_amount: condecimal(gt=0, max_digits=12, decimal_places=2)

    currency: constr(strip_whitespace=True, min_length=1, max_length=10) = "LKR"

    years_experience: conint(ge=0)

    is_anonymous: bool = False


class SalaryResponse(BaseModel):
    id: int
    job_title: str
    company: str
    location: str
    salary_amount: float
    currency: str
    years_experience: int
    status: str
    is_anonymous: bool
    created_at: datetime
    submitted_by: str

    class Config:
        orm_mode = True