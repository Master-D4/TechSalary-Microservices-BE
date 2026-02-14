from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.core import config, security, database
from app.models import user as models
from app.services import auth_service

# Use HTTPBearer instead of OAuth2PasswordBearer
security_scheme = HTTPBearer()


def get_current_user(
        db: Session = Depends(database.get_db),
        token: HTTPAuthorizationCredentials = Depends(security_scheme)  # CHANGE 2
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Extract the token string from the credentials object
        token_str = token.credentials

        payload = jwt.decode(
            token_str,
            config.settings.SECRET_KEY,
            algorithms=[config.settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    user = auth_service.get_user_by_id(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_admin_user(
        current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    is_admin = any(role.name == "ADMIN" for role in current_user.roles)
    if not is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user