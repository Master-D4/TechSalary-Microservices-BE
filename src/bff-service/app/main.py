from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, stats

app = FastAPI(title="TechSalary BFF", version="1.0.0")

# CORS CONFIGURATION
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["User Management"])

# Added stat-service Routers
app.include_router(stats.router, prefix="/api/v1", tags=["Stats"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "bff-service"}