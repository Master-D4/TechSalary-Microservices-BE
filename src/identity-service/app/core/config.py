import os
from pathlib import Path
from dotenv import load_dotenv


def load_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)


load_env()

class Settings:
    PROJECT_NAME: str = "Identity Service"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://myuser:mypassword@localhost:5433/techsalary_db",
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key_for_dev_only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
