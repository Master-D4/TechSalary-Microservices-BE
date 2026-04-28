from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# ✅ Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include vote routes
app.include_router(router, prefix="/vote", tags=["Vote"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "vote-service"}
