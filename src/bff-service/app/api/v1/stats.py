from typing import Optional
from fastapi import APIRouter, Response, Query

from app.services.stats_client import stats_client

router = APIRouter()


@router.get("/stats/filters")
async def get_filters(response: Response):
    data, status_code = await stats_client.forward_request(
        method="GET",
        path="/stats/filters"
    )
    response.status_code = status_code
    return data


@router.get("/stats/summary")
async def get_summary(
    response: Response,
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
):
    params = {
        "location": location,
        "job_title": job_title,
    }
    params = {k: v for k, v in params.items() if v is not None}

    data, status_code = await stats_client.forward_request(
        method="GET",
        path="/stats/summary",
        params=params
    )
    response.status_code = status_code
    return data


@router.get("/stats/percentiles")
async def get_percentiles(
    response: Response,
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
):
    params = {
        "location": location,
        "job_title": job_title,
    }
    params = {k: v for k, v in params.items() if v is not None}

    data, status_code = await stats_client.forward_request(
        method="GET",
        path="/stats/percentiles",
        params=params
    )
    response.status_code = status_code
    return data


@router.get("/stats/by-experience")
async def get_by_experience(
    response: Response,
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
):
    params = {
        "location": location,
        "job_title": job_title,
    }
    params = {k: v for k, v in params.items() if v is not None}

    data, status_code = await stats_client.forward_request(
        method="GET",
        path="/stats/by-experience",
        params=params
    )
    response.status_code = status_code
    return data


@router.get("/stats/top-roles")
async def get_top_roles(
    response: Response,
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=20),
):
    params = {
        "location": location,
        "job_title": job_title,
        "limit": limit,
    }
    params = {k: v for k, v in params.items() if v is not None}

    data, status_code = await stats_client.forward_request(
        method="GET",
        path="/stats/top-roles",
        params=params
    )
    response.status_code = status_code
    return data


@router.get("/stats/submissions-by-country")
async def get_submissions_by_country(
    response: Response,
    location: Optional[str] = Query(default=None),
    job_title: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=50),
):
    params = {
        "location": location,
        "job_title": job_title,
        "limit": limit,
    }
    params = {k: v for k, v in params.items() if v is not None}

    data, status_code = await stats_client.forward_request(
        method="GET",
        path="/stats/submissions-by-country",
        params=params
    )
    response.status_code = status_code
    return data