import sys
import os

# 1. Add the current directory to Python path so can import 'app'
sys.path.append(os.getcwd())

from app.core.database import engine
from app.models.user import Base


def reset_database():
    print("Connecting to database...")

    # This will DROP all tables defined in your models (Users, Roles, etc.)
    print("Dropping old tables...")
    Base.metadata.drop_all(bind=engine)

    # This will CREATE them again with the NEW columns
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)

    print("Database reset complete! You can now Signup.")


if __name__ == "__main__":
    reset_database()