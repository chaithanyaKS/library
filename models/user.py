from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Student(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(30))
