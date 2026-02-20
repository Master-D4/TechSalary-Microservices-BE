from fastapi import FastAPI
from app.api.v1.salary import router as salary_router

app = FastAPI(title="Salary Service")

app.include_router(salary_router, prefix="/api/v1/salary")


@app.get("/health")
def health():
    return {"status": "running"}


@app.get("/")
def root():
    return {"message": "Salary Service Running"}
