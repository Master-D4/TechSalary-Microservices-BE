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


def get_approved(db: Session):
    salaries = db.query(SalarySubmission).filter(
        SalarySubmission.status == "APPROVED"
    ).all()

    return [_apply_anonymization(salary) for salary in salaries]


def get_all(db: Session):
    salaries = db.query(SalarySubmission).all()
    return [_apply_anonymization(salary) for salary in salaries]