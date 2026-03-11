from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import List, Literal

from app.core.database import get_db
from app.core.config import settings
from app.schemas.salary import SalaryCreate, SalaryResponse
from app.services.salary_service import create_salary, get_approved, get_all
from app.models.salary import SalarySubmission

router = APIRouter()


@router.post("/submit", response_model=SalaryResponse)
def submit_salary(data: SalaryCreate, db: Session = Depends(get_db)):
    return create_salary(db, data)


@router.get("/approved", response_model=List[SalaryResponse])
def approved_salaries(db: Session = Depends(get_db)):
    return get_approved(db)


@router.get("/all", response_model=List[SalaryResponse])
def get_all_salaries(db: Session = Depends(get_db)):
    return get_all(db)


@router.patch("/internal/{submission_id}/status", response_model=SalaryResponse)
def update_salary_status(
    submission_id: int,
    status: Literal["APPROVED", "REJECTED"],
    db: Session = Depends(get_db),
    x_internal_token: str = Header(default=None)
):
    if x_internal_token != settings.INTERNAL_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    salary = db.query(SalarySubmission).filter(
        SalarySubmission.id == submission_id
    ).first()

    if not salary:
        raise HTTPException(status_code=404, detail="Salary not found")

    salary.status = status
    db.commit()
    db.refresh(salary)

    return salary