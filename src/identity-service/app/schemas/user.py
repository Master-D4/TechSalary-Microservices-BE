from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError
from typing import List, Optional, Any

# Base Schema
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# Input for Signup
class UserCreate(UserBase):
    password: str = Field(...)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            # raise ValueError('Password must be at least 8 characters long')
            raise PydanticCustomError(
                'password_too_short',
                'Password must be at least 8 characters long',
                {'min_length': 8}
            )
        return v

# Input for Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response Schema (Public Data)
class UserResponse(UserBase):
    id: int
    is_active: bool
    roles: List[str] = []

    class Config:
        from_attributes = True

    @field_validator('roles', mode='before')
    @classmethod
    def serialize_roles(cls, v: Any) -> List[str]:
        # If the incoming value is empty, return empty list
        if not v:
            return []

        # If the list contains Role objects (from SQLAlchemy), extract the name
        # We check the first item to see if it has a 'name' attribute
        first_item = v[0]
        if hasattr(first_item, 'name'):
            return [role.name for role in v]

        # If it's already a list of strings, just return it
        return v

class Token(BaseModel):
    access_token: str
    token_type: str

# Update Schema
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    # 'is_active' is reserved for Admin actions, but we can include it here
    # and filter it out in the API if needed.
    is_active: Optional[bool] = None

# Pagination Schema
class UserListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[UserResponse]

# Response for both Login and Signup
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse