from fastapi import APIRouter, HTTPException, Request, Response

from app.schemas.vote import ReportDelete, ReportRequest, VoteRequest
from app.services.vote_client import vote_client


router = APIRouter()


def require_auth_header(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    return auth_header


@router.post("/vote/Add")
async def create_vote(request: Request, payload: VoteRequest, response: Response):
    auth_header = require_auth_header(request)
    data, status_code = await vote_client.forward_request(
        method="POST",
        path="/Add",
        data=payload.model_dump(),
        headers={"Authorization": auth_header},
    )
    response.status_code = status_code
    return data


@router.delete("/vote/Delete")
async def delete_vote(request: Request, payload: VoteRequest, response: Response):
    auth_header = require_auth_header(request)
    data, status_code = await vote_client.forward_request(
        method="DELETE",
        path="/Delete",
        data=payload.model_dump(),
        headers={"Authorization": auth_header},
    )
    response.status_code = status_code
    return data


@router.post("/vote/Report")
async def create_report(request: Request, payload: ReportRequest, response: Response):
    auth_header = require_auth_header(request)
    data, status_code = await vote_client.forward_request(
        method="POST",
        path="/Report",
        data=payload.model_dump(),
        headers={"Authorization": auth_header},
    )
    response.status_code = status_code
    return data


@router.delete("/vote/Report")
async def delete_report(request: Request, payload: ReportDelete, response: Response):
    auth_header = require_auth_header(request)
    data, status_code = await vote_client.forward_request(
        method="DELETE",
        path="/Report",
        data=payload.model_dump(),
        headers={"Authorization": auth_header},
    )
    response.status_code = status_code
    return data
