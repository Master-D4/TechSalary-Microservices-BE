from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- SHARED MODELS ---
class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# --- INPUT SCHEMAS (Requests) ---
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# --- OUTPUT SCHEMAS (Responses) ---
class UserResponse(UserBase):
    id: int
    is_active: bool
    roles: List[str] = []

class UserListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[UserResponse]