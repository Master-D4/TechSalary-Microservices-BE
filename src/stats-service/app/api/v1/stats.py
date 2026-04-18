from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.stats import (
    FilterOptionsResponse,
    SummaryResponse,
    PercentilesResponse,
    ExperienceBucketItem,
    TopRoleItem,
    CountrySubmissionItem,
)
from app.services.stats_service import StatsService

router = APIRouter(tags=["Stats"])


@router.get("/stats/filters", response_model=FilterOptionsResponse)
def get_filters(db: Session = Depends(get_db)):
    return StatsService.get_filters(db=db)


@router.get("/stats/summary", response_model=SummaryResponse)
def get_summary(
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return StatsService.get_summary(
        db=db,
        location=location,
        job_title=job_title,
    )


@router.get("/stats/percentiles", response_model=PercentilesResponse)
def get_percentiles(
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return StatsService.get_percentiles(
        db=db,
        location=location,
        job_title=job_title,
    )


@router.get("/stats/by-experience", response_model=List[ExperienceBucketItem])
def get_by_experience(
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return StatsService.get_by_experience(
        db=db,
        location=location,
        job_title=job_title,
    )


@router.get("/stats/top-roles", response_model=List[TopRoleItem])
def get_top_roles(
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=20),
    db: Session = Depends(get_db),
):
    return StatsService.get_top_roles(
        db=db,
        location=location,
        job_title=job_title,
        limit=limit,
    )


@router.get("/stats/submissions-by-country", response_model=List[CountrySubmissionItem])
def get_submissions_by_country(
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return StatsService.get_submissions_by_country(
        db=db,
        location=location,
        job_title=job_title,
        limit=limit,
    )