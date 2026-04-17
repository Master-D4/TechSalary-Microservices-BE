from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...schemas.salary import SalaryResponse
from ...services.search_service import search_salaries

router = APIRouter()


@router.get("/search", response_model=List[SalaryResponse])
def search_salary(
    search: str | None = None,
    location: str | None = None,
    company: str | None = None,
    status: str | None = None,
    sortBy: str = "newest",
    db: Session = Depends(get_db)
):
    return search_salaries(db, search, location, company, status, sortBy)