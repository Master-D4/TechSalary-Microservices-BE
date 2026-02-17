import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Vote Service"
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:PostgreSQL%40123@localhost:5432/techsalary_db")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/techsalary_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key_for_dev_only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
