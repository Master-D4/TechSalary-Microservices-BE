from fastapi import FastAPI
from .api.routes import router
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Include vote routes
app.include_router(router, prefix="/vote", tags=["Vote"])

# from fastapi import FastAPI, Depends, HTTPException, Header
# from sqlalchemy.orm import Session
# from jose import jwt, JWTError, ExpiredSignatureError
# from typing import Optional
# from .database import SessionLocal
# from .schemas.vote import VoteRequest
# from .services.vote_service import create_vote
# from .core.config import settings

# app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def verify_token(token: str):
#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM]
#         )
#         user_id = payload.get("user_id")
#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         return user_id
#     except ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

# @app.post("/vote")
# def vote(
#     request: VoteRequest,
#     authorization: Optional[str] = Header(None, alias="Authorization"),
#     db: Session = Depends(get_db)
# ):
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Token required")
    
#     # Extract token
#     if authorization.startswith("Bearer "):
#         token = authorization[7:]  # Remove "Bearer " prefix
#     else:
#         token = authorization
    
#     if not token:
#         raise HTTPException(status_code=401, detail="Token required")
    
#     user_id = verify_token(token)
    
#     result = create_vote(db, request.submission_id, user_id, request.vote_type)
#     if "error" in result:
#         raise HTTPException(status_code=400, detail=result["error"])
    
#     return result

# # from fastapi import FastAPI, Depends, HTTPException, Header
# # from sqlalchemy.orm import Session
# # from jose import jwt, JWTError, ExpiredSignatureError
# # from .database import SessionLocal
# # from .schemas.vote import VoteRequest
# # from .services.vote_service import create_vote
# # from .core.config import settings

# # app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # def verify_token(token: str):
# #     try:
# #         payload = jwt.decode(
# #             token,
# #             settings.SECRET_KEY,
# #             algorithms=[settings.ALGORITHM]
# #         )
# #         return payload.get("user_id")
# #     except ExpiredSignatureError:
# #         raise HTTPException(status_code=401, detail="Token expired")
# #     except JWTError:
# #         raise HTTPException(status_code=401, detail="Invalid token")

# # @app.post("/vote")
# # def vote(
# #     request: VoteRequest,
# #     authorization: str = Header(None),
# #     db: Session = Depends(get_db)
# # ):
# #     if not authorization:
# #         raise HTTPException(status_code=401, detail="Token required")

# #     token = authorization.replace("Bearer ", "")
# #     user_id = verify_token(token)

# #     if not user_id:
# #         raise HTTPException(status_code=401, detail="Invalid token payload")

# #     result = create_vote(db, request.submission_id, user_id, request.vote_type)

# #     if "error" in result:
# #         raise HTTPException(status_code=400, detail=result["error"])

# #     return result
# # from fastapi import FastAPI, Depends, HTTPException, Header
# # from sqlalchemy.orm import Session
# # from .database import SessionLocal
# # from .schemas import VoteRequest
# # from .service import create_vote
# # from jose import jwt
# # import os

# # app = FastAPI()

# # SECRET_KEY = os.getenv("SECRET_KEY")
# # ALGORITHM = "HS256"

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()


# # def verify_token(token: str):
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         return payload.get("user_id")
# #     except:
# #         return None


# # @app.post("/vote")
# # def vote(
# #     request: VoteRequest,
# #     authorization: str = Header(None),
# #     db: Session = Depends(get_db)
# # ):

# #     if not authorization:
# #         raise HTTPException(status_code=401, detail="Token required")

# #     token = authorization.replace("Bearer ", "")
# #     user_id = verify_token(token)

# #     if not user_id:
# #         raise HTTPException(status_code=401, detail="Invalid token")

# #     result = create_vote(db, request.submission_id, user_id, request.vote_type)

# #     if "error" in result:
# #         raise HTTPException(status_code=400, detail=result["error"])

# #     return result