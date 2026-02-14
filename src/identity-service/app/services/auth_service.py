from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models import user as models
from app.schemas import user as schemas
from app.core import security


def create_user(db: Session, user_in: schemas.UserCreate):
    # 1. Check if Email Exists
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Check if Username Exists
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # 3. Fetch Default Role ('USER')
    # Note: We rely on init.sql having created this.
    # If not found, we fallback to creating it or erroring.
    user_role = db.query(models.Role).filter(models.Role.name == "USER").first()
    if not user_role:
        # Fallback mechanism if DB is empty
        user_role = models.Role(name="USER")
        db.add(user_role)
        db.commit()

    # 4. Hash Password
    hashed_pw = security.get_password_hash(user_in.password)

    # 5. Create User Object
    new_user = models.User(
        email=user_in.email,
        username=user_in.username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        password_hash=hashed_pw
    )

    # 6. Assign Role
    new_user.roles.append(user_role)

    # 7. Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not security.verify_password(password, user.password_hash):
        return None
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 10, search: str = None):
    query = db.query(models.User)

    # SEARCH LOGIC: Filter by username OR email
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            or_(
                models.User.username.ilike(search_fmt),
                models.User.email.ilike(search_fmt)
            )
        )

    total = query.count()
    users = query.offset(skip).limit(limit).all()

    return {"total": total, "items": users}


def update_user(db: Session, user_id: int, update_data: schemas.UserUpdate):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    # Convert Pydantic model to dict, excluding None values
    update_dict = update_data.model_dump(exclude_unset=True)

    # Handle Password Hashing if password is being updated
    if 'password' in update_dict:
        update_dict['password_hash'] = security.get_password_hash(update_dict.pop('password'))

    for key, value in update_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    # Hard Delete (Removes row)
    # Note: If this user has linked data in other services, those might break
    # (Microservice constraint). But within Identity, this is safe.
    db.delete(user)
    db.commit()
    return True


def deactivate_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    user.is_active = False
    db.commit()
    db.refresh(user)
    return user