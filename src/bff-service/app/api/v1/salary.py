from fastapi import APIRouter, Request, Response
from app.services.salary_client import salary_client

router = APIRouter()


@router.get("/salary/all")
async def get_all_salaries(request: Request, response: Response):
    auth_header = request.headers.get("Authorization")

    data, status_code = await salary_client.forward_request(
        method="GET",
        path="/all",
        headers={"Authorization": auth_header} if auth_header else None
    )

    response.status_code = status_code
    return data


@router.get("/salary/approved")
async def get_approved_salaries(request: Request, response: Response):
    auth_header = request.headers.get("Authorization")

    data, status_code = await salary_client.forward_request(
        method="GET",
        path="/approved",
        headers={"Authorization": auth_header} if auth_header else None
    )

    response.status_code = status_code
    return data


@router.post("/salary/")
async def create_salary(request: Request, response: Response):
    body = await request.json()
    auth_header = request.headers.get("Authorization")

    data, status_code = await salary_client.forward_request(
        method="POST",
        path="/",
        data=body,
        headers={"Authorization": auth_header} if auth_header else None
    )

    response.status_code = status_code
    return data