from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.inventory import Inventory


class Book(Base):
    __tablename__ = "book"
    isbn: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    subject: Mapped[str]

    inventory: Mapped[Inventory] = relationship(back_populates="book")
