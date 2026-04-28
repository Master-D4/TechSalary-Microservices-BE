from fastapi import FastAPI
from app.api.v1 import search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Search Service",
    version="1.0.0"
)

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

app.include_router(search.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "search-service"
    }