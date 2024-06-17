from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.book import Book


class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey(column=Book.isbn), unique=True)
    count: Mapped[int] = mapped_column(default=0)
    book: Mapped[Book] = relationship(back_populates="inventory")
