from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    fullName: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    profilePic: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    profile_pic: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True