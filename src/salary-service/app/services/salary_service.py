from sqlalchemy.orm import Session
from app.models.salary import SalarySubmission


def create_salary(db: Session, data):
    payload = data.dict()
    payload["status"] = "PENDING"

    salary = SalarySubmission(**payload)
    db.add(salary)
    db.commit()
    db.refresh(salary)

    return salary


def serialize_salary(salary: SalarySubmission, is_logged_in: bool):
    return {
        "id": salary.id,
        "job_title": salary.job_title,
        "company": salary.company,
        "location": salary.location,
        "salary_amount": float(salary.salary_amount),
        "currency": salary.currency,
        "years_experience": salary.years_experience,
        "status": salary.status,
        "created_at": salary.created_at,
        "submitted_by": "User" if is_logged_in else "Anonymous",
        "is_anonymous": salary.is_anonymous,
    }


def get_approved(
    db: Session,
    is_logged_in: bool,
    limit: int = 20,
    offset: int = 0,
    status: str | None = None,
    job_title: str | None = None,
    company: str | None = None,
    location: str | None = None,
):
    query = db.query(SalarySubmission).filter(
        SalarySubmission.status == "APPROVED"
    )

    if job_title:
        query = query.filter(SalarySubmission.job_title.ilike(f"%{job_title}%"))

    if company:
        query = query.filter(SalarySubmission.company.ilike(f"%{company}%"))

    if location:
        query = query.filter(SalarySubmission.location.ilike(f"%{location}%"))

    salaries = (
        query.order_by(SalarySubmission.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [serialize_salary(s, is_logged_in) for s in salaries]


def get_all(
    db: Session,
    is_logged_in: bool,
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    job_title: str | None = None,
    company: str | None = None,
    location: str | None = None,
):
    query = db.query(SalarySubmission)

    if status:
        query = query.filter(SalarySubmission.status == status)

    if job_title:
        query = query.filter(SalarySubmission.job_title.ilike(f"%{job_title}%"))

    if company:
        query = query.filter(SalarySubmission.company.ilike(f"%{company}%"))

    if location:
        query = query.filter(SalarySubmission.location.ilike(f"%{location}%"))

    salaries = (
        query.order_by(SalarySubmission.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [serialize_salary(s, is_logged_in) for s in salaries]