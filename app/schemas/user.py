from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user_role import UserRole


class UserBase(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    user_role: Optional[UserRole]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
