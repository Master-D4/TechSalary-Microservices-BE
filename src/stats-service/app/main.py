from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.stats import router as stats_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

origins = ["*"] if settings.CORS_ORIGINS == "*" else [
    origin.strip() for origin in settings.CORS_ORIGINS.split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(stats_router, prefix="/api/v1")