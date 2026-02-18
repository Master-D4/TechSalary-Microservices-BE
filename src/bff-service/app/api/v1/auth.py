from fastapi import APIRouter, Response
from app.services.identity_client import identity_client
from app.schemas.auth import UserLogin, UserSignup


router = APIRouter()


@router.post("/auth/signup")
async def user_signup(user_in: UserSignup, response: Response):  # <--- Use Schema
    # FastAPI has already validated the JSON body for us
    # user_in is now a Pydantic object

    data, status_code = await identity_client.forward_request(
        method="POST",
        path="/auth/signup",
        data=user_in.model_dump()  # Convert Pydantic model to Dict
    )

    response.status_code = status_code
    return data


@router.post("/auth/login")
async def user_login(user_credentials: UserLogin, response: Response):  # <--- Use Schema
    data, status_code = await identity_client.forward_request(
        method="POST",
        path="/auth/login",
        data=user_credentials.model_dump()
    )

    response.status_code = status_code
    return data