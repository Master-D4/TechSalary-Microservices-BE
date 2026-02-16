import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Salary Service"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    INTERNAL_TOKEN: str = os.getenv("INTERNAL_TOKEN")

settings = Settings()
