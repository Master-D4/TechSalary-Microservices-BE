from sqlalchemy.orm import Session
from app.models.salary import SalarySubmission

def create_salary(db: Session, data):
    salary = SalarySubmission(**data.dict())
    db.add(salary)
    db.commit()
    db.refresh(salary)
    return salary

def get_approved(db: Session):
    return db.query(SalarySubmission).filter(
        SalarySubmission.status == "APPROVED"
    ).all()
