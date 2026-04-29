from sqlalchemy.orm import Session
from app.models.salary import SalarySubmission


def create_salary(db: Session, data):
    try:
        payload = data.dict()
        payload["status"] = "PENDING"

        if "salary_amount" in payload:
            payload["salary_amount"] = float(payload["salary_amount"])

        salary = SalarySubmission(**payload)

        db.add(salary)
        db.commit()
        db.refresh(salary)

        return {
            "id": salary.id,
            "job_title": salary.job_title,
            "company": salary.company,
            "location": salary.location,
            "salary_amount": float(salary.salary_amount),
            "currency": salary.currency,
            "years_experience": salary.years_experience,
            "status": salary.status,
            "is_anonymous": salary.is_anonymous,
            "created_at": salary.created_at,
            "submitted_by": "Anonymous"
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise

# def serialize_salary(salary: SalarySubmission, is_logged_in: bool):
#     return {
#         "id": salary.id,
#         "job_title": salary.job_title,
#         "company": salary.company,
#         "location": salary.location,
#         "salary_amount": float(salary.salary_amount),
#         "currency": salary.currency,
#         "years_experience": salary.years_experience,
#         "status": salary.status,
#         "created_at": salary.created_at,
#         "submitted_by": "User" if is_logged_in else "Anonymous",
#         "is_anonymous": salary.is_anonymous,
#     }

def serialize_salary(salary, is_logged_in: bool = False):
    # 1. If the data arrives as a Python Dictionary
    if isinstance(salary, dict):
        is_anon = salary.get("is_anonymous", False)
        return {
            "id": salary.get("id"),
            "job_title": salary.get("job_title"),
            "company": salary.get("company"),
            "location": salary.get("location"),
            "salary_amount": float(salary.get("salary_amount", 0)),
            "currency": salary.get("currency"),
            "years_experience": salary.get("years_experience"),
            "status": salary.get("status"),
            "created_at": salary.get("created_at"),
            "submitted_by": "Anonymous" if is_anon else "User",
            "is_anonymous": is_anon,
        }

    # 2. If the data arrives as a SQLAlchemy Object
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
        "submitted_by": "Anonymous" if salary.is_anonymous else "User",
        "is_anonymous": salary.is_anonymous,
    }

def get_approved(
    db: Session,
    is_logged_in: bool,
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