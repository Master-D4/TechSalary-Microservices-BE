from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core import database, config, security
from app.schemas import user as schemas
from app.services import auth_service

router = APIRouter()

# 1. Register User
@router.post("/signup", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_user = auth_service.create_user(db=db, user_in=user_in)

    return create_auth_response(new_user)

# 2. User Login
@router.post("/login", response_model=schemas.AuthResponse)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = auth_service.authenticate_user(db, email=user_credentials.email, password=user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_auth_response(user)

# 3. Helper function to generate token response
def create_auth_response(user):
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    role_names = [role.name for role in user.roles]

    access_token = security.create_access_token(
        data={"sub": str(user.id), "roles": role_names},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }