from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core import database
from app.schemas import user as schemas
from app.services import auth_service
from app.api import deps
from app.models import user as models

router = APIRouter()

# 1. GET ALL USERS
@router.get("/", response_model=schemas.UserListResponse)
def read_users(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    result = auth_service.get_all_users(db, skip=skip, limit=limit, search=search)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1,
        "size": limit,
        "items": result["items"]
    }

# 2. UPDATE USER
@router.put("/me", response_model=schemas.UserResponse)
def update_self(
    user_data: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # Get the ID from the token
    updated_user = auth_service.update_user(db, current_user.id, user_data)
    return updated_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user_endpoint(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # Optional: Check if user is updating themselves OR is Admin
    # if current_user.id != user_id and not is_admin(current_user):
    #    raise HTTPException(status_code=403, detail="Not authorized")

    updated_user = auth_service.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# 3. DEACTIVATE USER
@router.patch("/{user_id}/deactivate", response_model=schemas.UserResponse)
def deactivate_user_endpoint(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    user = auth_service.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 4. DELETE USER
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_admin_user)
):
    success = auth_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None