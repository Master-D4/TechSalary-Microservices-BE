from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, salary,search

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
app.include_router(salary.router, prefix="/api/v1", tags=["Salary"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "bff-service"}