from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    email: str
    name: str


class User(UserBase):
    class Meta:
        orm_mode = True
