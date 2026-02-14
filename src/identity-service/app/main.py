from fastapi import FastAPI
from app.api.v1 import auth
from app.core import database
# Ensure models are imported so SQLAlchemy sees them
from app.models import user as models

# Create Tables (For local dev only - in Prod we use migration scripts like Alembic)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Identity Service", version="1.0.0")

# Include the Router
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "identity-service"}