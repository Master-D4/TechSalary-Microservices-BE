from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users
from app.core import database
from app.models import user as models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Identity Service", version="1.0.0")

# ADD CORS CONFIGURATION
origins = [
    "http://localhost:3000",
    "http://192.168.1.182:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Allows requests from these origins
    allow_credentials=True,    # Allows cookies/auth headers
    # allow_methods=["*"],       # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],       # Allows all headers (Content-Type, Authorization, etc.)
)

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
    # return {"status": "healthy", "service": "identity-service"}
    # Triggering CI/CD pipeline
    return {"status": "Healthy Triggering CI/CD pipeline", "service": "identity-service"}