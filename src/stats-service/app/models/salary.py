from sqlalchemy import Boolean, Column, Integer, Numeric, String, TIMESTAMP, text

from app.core.database import Base


class SalarySubmission(Base):
    __tablename__ = "salary_submissions"
    __table_args__ = {"schema": "salary"}

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    salary_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False, server_default=text("'LKR'"))
    years_experience = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, server_default=text("'PENDING'"))
    is_anonymous = Column(Boolean, nullable=False, server_default=text("FALSE"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))