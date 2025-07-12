# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    skills_offered: Optional[str] = None
    skills_wanted: Optional[str] = None
    is_public: Optional[bool] = True

    class Config:
        from_attributes = True # Pydantic v2 replaces orm_mode with from_attributes

class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    skills_offered: Optional[str] = None
    skills_wanted: Optional[str] = None
    is_public: Optional[bool] = True
class TokenWithUser(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
class Token(BaseModel):
    access_token: str
    token_type: str
# app/schemas.py (add at the bottom)

class SwapRequestCreate(BaseModel):
    target_id: int
    skill_offered: str
    skill_wanted: str
    message: str

