from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RoleCreate(RoleBase):
    name: str


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True
