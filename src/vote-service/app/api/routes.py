from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..database import SessionLocal
from ..schemas.vote import ReportDelete, ReportRequest, VoteRequest
from ..services.vote_service import create_report, create_vote, delete_report_service, delete_vote_service
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


@router.post("/Add")
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
    result = create_vote(db, request.salary_submission_id, user_id, request.vote_type)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


# FastAPI route
@router.delete("/Delete")
def delete_vote(
    request: VoteRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    # Get user_id from token
    user_id = verify_token(token)

    # Call service to delete vote
    result = delete_vote_service(db, request.salary_submission_id, user_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
@router.post("/Report")
def report(
    request: ReportRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    user_id = verify_token(token)

    return create_report(db, request.salary_submission_id, user_id,request.reason)


@router.delete("/Report")
def delete_report(
    request: ReportDelete,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    user_id = verify_token(token)

    return delete_report_service(db, request.salary_submission_id, user_id)
