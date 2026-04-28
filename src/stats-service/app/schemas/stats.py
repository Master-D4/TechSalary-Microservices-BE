from typing import List, Optional

from pydantic import BaseModel


class FilterOptionsResponse(BaseModel):
    countries: List[str]
    roles: List[str]


class SummaryResponse(BaseModel):
    total_entries: int
    average_salary: Optional[float]
    median_salary: Optional[float]


class PercentilesResponse(BaseModel):
    p25_salary: Optional[float]
    p50_salary: Optional[float]
    p75_salary: Optional[float]
    p90_salary: Optional[float]


class ExperienceBucketItem(BaseModel):
    experience_range: str
    count: int
    average_salary: Optional[float]


class TopRoleItem(BaseModel):
    job_title: str
    average_salary: float
    count: int


class CountrySubmissionItem(BaseModel):
    country: str
    count: int