from fastapi import APIRouter, Request, Response, HTTPException, status
from typing import Optional

from app.services.identity_client import identity_client
from app.schemas.user import UserUpdate, UserResponse, UserListResponse

router = APIRouter()


# --- UPDATE OWN PROFILE ---
@router.put("/users/me", response_model=UserResponse)
async def update_user_profile(
        request: Request,
        user_data: UserUpdate,
        response: Response
):
    """
    Update the logged-in user's profile (Self-Service).
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    data, status_code = await identity_client.forward_request(
        method="PUT",
        path="/users/me",
        data=user_data.model_dump(exclude_unset=True),
        headers={"Authorization": auth_header}
    )

    response.status_code = status_code
    return data


# --- LIST ALL USERS (Admin/Staff) ---
@router.get("/users/", response_model=UserListResponse)
async def list_users(
        request: Request,
        response: Response,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None
):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    skip = (page - 1) * limit

    query_params = f"?skip={skip}&limit={limit}"
    if search:
        query_params += f"&search={search}"

    data, status_code = await identity_client.forward_request(
        method="GET",
        path=f"/users/{query_params}",
        headers={"Authorization": auth_header}
    )

    response.status_code = status_code
    return data


# --- UPDATE USER BY ID (Admin) ---
@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_by_admin(
        user_id: int,
        user_data: UserUpdate,
        request: Request,
        response: Response
):
    """
    Admin Endpoint: Update a specific user by their ID.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    data, status_code = await identity_client.forward_request(
        method="PUT",
        path=f"/users/{user_id}",
        data=user_data.model_dump(exclude_unset=True),
        headers={"Authorization": auth_header}
    )

    response.status_code = status_code
    return data


# --- DEACTIVATE USER (Admin) ---
@router.patch("/users/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
        user_id: int,
        request: Request,
        response: Response
):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    data, status_code = await identity_client.forward_request(
        method="PATCH",
        path=f"/users/{user_id}/deactivate",
        headers={"Authorization": auth_header}
    )

    response.status_code = status_code
    return data


# --- DELETE USER (Admin) ---
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        request: Request,
        response: Response
):
    """
    Admin Endpoint: Hard delete a user.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    data, status_code = await identity_client.forward_request(
        method="DELETE",
        path=f"/users/{user_id}",
        headers={"Authorization": auth_header}
    )

    response.status_code = status_code
    return data