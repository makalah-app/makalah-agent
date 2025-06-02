"""
User data models and schemas
Agent-Makalah Backend Authentication
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    """Base user information"""
    email: str  # Changed from EmailStr to str temporarily


class UserCreate(UserBase):
    """Data required for user registration"""
    password: str


class UserInDB(UserBase):
    """User data as stored in the database"""
    id: uuid.UUID
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    """User data that can be publicly exposed"""
    id: uuid.UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update data"""
    email: Optional[str] = None  # Changed from EmailStr to str temporarily
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored within the JWT"""
    email: Optional[str] = None
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request data"""
    email: str  # Changed from EmailStr to str temporarily
    password: str


class UserResponse(BaseModel):
    """Standard user response"""
    user: UserPublic
    message: str = "Success" 