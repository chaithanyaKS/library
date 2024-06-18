from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str


class User(UserBase):
    class Meta:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    is_active: bool | None = True
    is_admin: bool | None = False
