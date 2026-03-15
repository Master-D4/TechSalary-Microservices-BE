from sqlalchemy.orm import Session
from ..models.salary import Salary


def search_salaries(db: Session, country=None, company=None, role=None, level=None):

    query = db.query(Salary)

    if country:
        query = query.filter(Salary.location.ilike(f"%{country}%"))

    if company:
        query = query.filter(Salary.company.ilike(f"%{company}%"))

    if role:
        query = query.filter(Salary.job_title.ilike(f"%{role}%"))

    if level:
        query = query.filter(Salary.years_experience.ilike(f"%{level}%"))

    return query.all()