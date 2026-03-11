from sqlalchemy.orm import Session
from app.models.salary import SalarySubmission


def _apply_anonymization(salary: SalarySubmission):
    if salary.is_anonymous:
        salary.company = "Anonymous"
    return salary


def create_salary(db: Session, data):
    payload = data.dict()

    # Always store new submissions as PENDING
    payload["status"] = "PENDING"

    salary = SalarySubmission(**payload)
    db.add(salary)
    db.commit()
    db.refresh(salary)
    return salary


def get_approved(
    db: Session,
    limit: int = 20,
    offset: int = 0,
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

    return [_apply_anonymization(salary) for salary in salaries]


def get_all(
    db: Session,
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

    return [_apply_anonymization(salary) for salary in salaries]