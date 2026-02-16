from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class SalarySubmission(Base):
    __tablename__ = "salary_submissions"
    __table_args__ = {"schema": "salary"}

    id = Column(Integer, primary_key=True, index=True)

    job_title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)

    salary_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="LKR")

    years_experience = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    is_anonymous = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
