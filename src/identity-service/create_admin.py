import sys
import os

sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.core import database, security
from app.models import user as models

def create_super_user():
    db = next(database.get_db())

    email = input("Enter Admin Email: ")
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    # 1. Check if user exists
    if db.query(models.User).filter(models.User.email == email).first():
        print("Error: User with this email already exists.")
        return

    # 2. Get Admin Role
    admin_role = db.query(models.Role).filter(models.Role.name == "ADMIN").first()
    if not admin_role:
        print("'ADMIN' role not found. Creating it...")
        admin_role = models.Role(name="ADMIN")
        db.add(admin_role)
        db.commit()

    # 3. Create User
    hashed_pw = security.get_password_hash(password)
    new_admin = models.User(
        email=email,
        username=username,
        password_hash=hashed_pw,
        is_active=True
    )

    # 4. Assign Role
    new_admin.roles.append(admin_role)

    db.add(new_admin)
    db.commit()
    print(f"Admin user '{username}' created successfully!")

if __name__ == "__main__":
    create_super_user()