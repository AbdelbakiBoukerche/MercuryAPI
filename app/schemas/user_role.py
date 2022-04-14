from typing import Optional

from app.schemas.role import Role
from pydantic import BaseModel


class UserRoleBase(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(UserRoleBase):
    role_id: int


class UserRole(UserRoleBase):
    role: Role

    class Config:
        orm_mode = True
