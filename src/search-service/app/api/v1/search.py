from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...schemas.salary import SalaryResponse
from ...services.search_service import search_salaries

router = APIRouter()


@router.get("/search", response_model=List[SalaryResponse])
def search(
    location: str = None,
    company: str = None,
    job_title: str = None,
    years_experience: int = None,
    db: Session = Depends(get_db)
):
    return search_salaries(db, location, company, job_title, years_experience)