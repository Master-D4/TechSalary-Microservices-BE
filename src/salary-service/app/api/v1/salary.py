from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Literal, Optional

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
def approved_salaries(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    job_title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
):
    return get_approved(
        db=db,
        limit=limit,
        offset=offset,
        job_title=job_title,
        company=company,
        location=location,
    )


@router.get("/all", response_model=List[SalaryResponse])
def get_all_salaries(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: Optional[Literal["PENDING", "APPROVED", "REJECTED"]] = None,
    job_title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
):
    return get_all(
        db=db,
        limit=limit,
        offset=offset,
        status=status,
        job_title=job_title,
        company=company,
        location=location,
    )


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