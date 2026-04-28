import os
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    # salary-service/.env (3 levels up from app/core/config.py)
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)


load_env()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://myuser:mypassword@localhost:5433/techsalary_db",
    )
    INTERNAL_TOKEN: str = os.getenv("INTERNAL_TOKEN", "dev_internal_token")


settings = Settings()
