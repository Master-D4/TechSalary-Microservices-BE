import os
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    # salary-service/.env (3 levels up from app/core/config.py)
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)


load_env()


class Settings:
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    INTERNAL_TOKEN: str | None = os.getenv("INTERNAL_TOKEN")


settings = Settings()
