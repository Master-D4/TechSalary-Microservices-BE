from sqlalchemy.orm import Session
from ..models.salary import Salary
from sqlalchemy import cast, String


def search_salaries(db: Session, search=None, country=None, company=None, status=None, sort_by=None):

    query = db.query(Salary)

    if search:
        query = query.filter(
            (Salary.location.ilike(f"%{search}%")) |
            (Salary.company.ilike(f"%{search}%")) |
            (Salary.job_title.ilike(f"%{search}%")) |
            (cast(Salary.years_experience, String).ilike(f"%{search}%"))
        )
    if country:
        query = query.filter(Salary.location == country)

    if company:
        query = query.filter(Salary.company == company)

    if status:
        query = query.filter(Salary.status == status)

    if sort_by == "newest":
        query = query.order_by(Salary.created_at.desc())
    elif sort_by == "highest":
        query = query.order_by(Salary.salary_amount.desc())

    return query.all()