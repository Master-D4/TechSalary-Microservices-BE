from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.salary import router as salary_router

app = FastAPI(title="Salary Service")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API router
app.include_router(salary_router, prefix="/api/v1/salary")

# Health check
@app.get("/health")
def health():
    return {"status": "running"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "Salary Service Running"}