from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from app.core import database, config, security
from app.schemas import user as schemas
from app.services import auth_service

router = APIRouter()


@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Call the service layer
    return auth_service.create_user(db=db, user_in=user)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = auth_service.authenticate_user(db, email=user_credentials.email, password=user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create Token
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # We include 'roles' in the token so other services know who this is without querying DB
    role_names = [role.name for role in user.roles]

    access_token = security.create_access_token(
        data={"sub": str(user.id), "email": user.email, "roles": role_names},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=schemas.UserListResponse)
def read_users(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    result = auth_service.get_all_users(db, skip=skip, limit=limit, search=search)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1,
        "size": limit,
        "items": result["items"]
    }


@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user_endpoint(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(database.get_db)
):
    updated_user = auth_service.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.patch("/users/{user_id}/deactivate", response_model=schemas.UserResponse)
def deactivate_user_endpoint(user_id: int, db: Session = Depends(database.get_db)):
    user = auth_service.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(database.get_db)):
    success = auth_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None