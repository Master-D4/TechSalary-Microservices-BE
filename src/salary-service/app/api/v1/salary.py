from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.salary import SalaryCreate, SalaryResponse
from app.services.salary_service import create_salary, get_approved
from app.models.salary import SalarySubmission

router = APIRouter()


@router.post("/submit", response_model=SalaryResponse)
def submit_salary(data: SalaryCreate, db: Session = Depends(get_db)):
    return create_salary(db, data)

@router.get("/all",response_model=List[SalaryResponse])
def get_all_salaries(db:Session=Depends(get_db)):
    return db.query(SalarySubmission).all()

@router.get("/approved", response_model=List[SalaryResponse])
def approved_salaries(db: Session = Depends(get_db)):
    return get_approved(db)
