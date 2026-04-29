from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.salary import SalaryCreate, SalaryResponse
from app.services import salary_service
from app.services.salary_service import create_salary, serialize_salary


router = APIRouter()

# @router.post("/", response_model=SalaryResponse)
# def create_salary(data: SalaryCreate, db: Session = Depends(get_db)):
#     return salary_service.create_salary(db, data)


@router.post("/", response_model=SalaryResponse)
def add_salary(data: SalaryCreate, db: Session = Depends(get_db)):
    # 1. Save to database
    new_salary = create_salary(db, data)

    # 2. Dynamically determine the visibility based on the payload
    # If is_anonymous is True, this becomes False. If False, it becomes True.
    user_visibility = not data.is_anonymous

    # 3. Format it properly with dynamic visibility!
    return serialize_salary(new_salary, is_logged_in=user_visibility)


@router.get("/approved",response_model=list[SalaryResponse])
def get_approved_salaries(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    job_title: str | None = None,
    company: str | None = None,
    location: str | None = None,
):
    is_logged_in = request.headers.get("Authorization") is not None

    return salary_service.get_approved(
        db=db,
        is_logged_in=is_logged_in,
        limit=limit,
        offset=offset,
        job_title=job_title,
        company=company,
        location=location,
    )


@router.get("/all",response_model=list[SalaryResponse])
def get_all_salaries(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    job_title: str | None = None,
    company: str | None = None,
    location: str | None = None,
):
    is_logged_in = request.headers.get("Authorization") is not None

    return salary_service.get_all(
        db=db,
        is_logged_in=is_logged_in,
        limit=limit,
        offset=offset,
        status=status,
        job_title=job_title,
        company=company,
        location=location,
    )