from fastapi import APIRouter, Response
from app.services.search_client import search_client


router = APIRouter()

@router.get("/search")
async def search_salary(
        response: Response,
        search: str | None = None,
        location: str | None = None,
        company: str | None = None,
        status: str | None = None,
        sortBy: str = "newest",
        page: int = 1,
        limit: int = 20,
):
    params = {
        "search": search,
        "location": location,
        "company": company,
        "status": status,
        "sortBy": sortBy,
        "page": page,
        "limit": limit,
    }
    params = {key: value for key, value in params.items() if value is not None}

    data, status_code = await search_client.forward_request(
        method="GET",
        path="/search",
        params=params
    )
    response.status_code = status_code
    return data

@router.get("/search/filters")
async def get_filters(response: Response):
    data, status_code = await search_client.forward_request(
        method="GET",
        path="/search/filters"
    )
    response.status_code = status_code
    return data
