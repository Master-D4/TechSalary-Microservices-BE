from fastapi import FastAPI
from app.api.v1 import auth, users
from app.core import database
from app.models import user as models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Identity Service", version="1.0.0")

# 1. Auth Router (Prefix: /api/v1/auth)
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

# 2. Users Router (Prefix: /api/v1/users)
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["User Management"]
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "identity-service"}