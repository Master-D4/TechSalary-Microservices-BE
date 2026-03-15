from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime
from ..core.database import Base


class Salary(Base):
    __tablename__ = "salary_submissions"
    __table_args__ = {"schema": "salary"}

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    company = Column(String)
    location = Column(String)
    salary_amount = Column(Numeric)
    currency = Column(String)
    years_experience = Column(Integer)
    status = Column(String)
    is_anonymous = Column(Boolean)
    created_at = Column(DateTime)
