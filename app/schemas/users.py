from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    address: str
    state: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    address: str
    state: str
    image_url: Optional[str] = None
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str