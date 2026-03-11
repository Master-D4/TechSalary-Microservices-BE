from sqlalchemy.orm import Session
from app.models.salary import SalarySubmission


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
    return db.query(SalarySubmission).filter(
        SalarySubmission.status == "APPROVED"
    ).all()