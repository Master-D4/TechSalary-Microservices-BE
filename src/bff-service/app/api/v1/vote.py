from fastapi import APIRouter, Request, Response

from app.services.vote_client import vote_client

router = APIRouter()


def get_auth_headers(request: Request):
    auth_header = request.headers.get("Authorization")
    return {"Authorization": auth_header} if auth_header else None


@router.post("/vote/Add")
async def create_vote(request: Request, response: Response):
    body = await request.json()

    data, status_code = await vote_client.forward_request(
        method="POST",
        path="/Add",
        data=body,
        headers=get_auth_headers(request)
    )

    response.status_code = status_code
    return data


@router.delete("/vote/Delete")
async def delete_vote(request: Request, response: Response):
    body = await request.json()

    data, status_code = await vote_client.forward_request(
        method="DELETE",
        path="/Delete",
        data=body,
        headers=get_auth_headers(request)
    )

    response.status_code = status_code
    return data


@router.post("/vote/Report")
async def create_report(request: Request, response: Response):
    body = await request.json()

    data, status_code = await vote_client.forward_request(
        method="POST",
        path="/Report",
        data=body,
        headers=get_auth_headers(request)
    )

    response.status_code = status_code
    return data


@router.delete("/vote/Report")
async def delete_report(request: Request, response: Response):
    body = await request.json()

    data, status_code = await vote_client.forward_request(
        method="DELETE",
        path="/Report",
        data=body,
        headers=get_auth_headers(request)
    )

    response.status_code = status_code
    return data


@router.get("/vote/State/{salary_submission_id}")
async def get_user_interaction_state(
    salary_submission_id: int,
    request: Request,
    response: Response
):
    data, status_code = await vote_client.forward_request(
        method="GET",
        path=f"/State/{salary_submission_id}",
        headers=get_auth_headers(request)
    )

    response.status_code = status_code
    return data
