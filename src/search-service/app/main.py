from fastapi import FastAPI
from app.api.v1 import search

app = FastAPI(
    title="Search Service",
    version="1.0.0"
)

app.include_router(search.router, prefix="/api/v1/salary")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "search-service"
    }