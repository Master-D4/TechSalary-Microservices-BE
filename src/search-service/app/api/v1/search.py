from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...schemas.salary import SalaryListResponse
from ...services.search_service import search_salaries
from ...services.search_service import get_filter_items

router = APIRouter()


@router.get("/search", response_model=SalaryListResponse)
def search_salary(
    search: str | None = None,
    location: str | None = None,
    company: str | None = None,
    status: str | None = None,
    sortBy: str = "newest",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return search_salaries(db, search, location, company, status, sortBy, page, limit)


@router.get("/filters")
def get_filters(db: Session = Depends(get_db)):

    return get_filter_items(db)