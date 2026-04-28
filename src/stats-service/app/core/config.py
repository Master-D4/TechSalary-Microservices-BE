from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "stats-service"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/salarydb"
    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file="stats_service.env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()