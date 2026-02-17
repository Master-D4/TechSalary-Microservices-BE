from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..database import SessionLocal
from ..schemas.vote import VoteRequest
from ..services.vote_service import create_vote
from ..core import config

router = APIRouter()
bearer_scheme = HTTPBearer()

# -------------------------------
# Database dependency
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# Verify JWT token
# -------------------------------
def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            config.settings.SECRET_KEY,
            algorithms=[config.settings.ALGORITHM]
        )
        user_id = payload.get("sub")  # ✅ User ID is stored in "sub"
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -------------------------------
# Vote Endpoint
# -------------------------------
@router.post("/")
def vote(
    request: VoteRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    # Get user_id from token
    user_id = verify_token(token)

    # Call service to create vote
    result = create_vote(db, request.submission_id, user_id, request.vote_type)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
# from fastapi import APIRouter, Depends, HTTPException, Header
# from sqlalchemy.orm import Session
# from typing import Optional
# from jose import jwt, JWTError, ExpiredSignatureError
# from ..database import SessionLocal
# from ..schemas.vote import VoteRequest
# from ..services.vote_service import create_vote
# from ..core import config

# router = APIRouter()

# # -------------------------------
# # Database dependency
# # -------------------------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # -------------------------------
# # Verify JWT token
# # -------------------------------
# def verify_token(token: str):
#     try:
#         payload = jwt.decode(
#             token,
#             config.settings.SECRET_KEY,
#             algorithms=[config.settings.ALGORITHM]
#         )
#         user_id = payload.get("sub")  # ✅ User ID is stored in "sub"
#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         return user_id
#     except ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# # -------------------------------
# # Vote Endpoint
# # -------------------------------
# @router.post("/")
# def vote(
#     request: VoteRequest,
#     authorization: Optional[str] = Header(None, alias="Authorization"),
#     db: Session = Depends(get_db)
# ):
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Token required")

#     # Remove "Bearer " prefix if exists
#     token = authorization[7:] if authorization.startswith("Bearer ") else authorization

#     if not token:
#         raise HTTPException(status_code=401, detail="Token required")

#     # Get user_id from token
#     user_id = verify_token(token)

#     # Call service to create vote
#     result = create_vote(db, request.submission_id, user_id, request.vote_type)

#     if "error" in result:
#         raise HTTPException(status_code=400, detail=result["error"])

#     return result