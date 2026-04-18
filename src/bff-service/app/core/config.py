from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TechSalary BFF"

    # URL of the internal Identity Service
    # For Docker/K8s, this will be "http://identity-service:8001"
    IDENTITY_SERVICE_URL: str = "http://localhost:8001/api/v1"
    STAT_SERVICE_URL: str = "http://localhost:8006/api/v1"

    class Config:
        case_sensitive = True

settings = Settings()