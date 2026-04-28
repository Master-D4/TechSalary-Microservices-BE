from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from app.database import Base


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {"schema": "community"}

    id = Column(Integer, primary_key=True, index=True)
    salary_submission_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    vote_type = Column(String(10), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = {"schema": "community"}

    id = Column(Integer, primary_key=True, index=True)
    salary_submission_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
