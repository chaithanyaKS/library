from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(default=0)
    borrowed_count: Mapped[int] = mapped_column(default=0)
    book_id: Mapped[int] = mapped_column(ForeignKey(column="book.isbn"), unique=True)
    book: Mapped["Book"] = relationship(back_populates="inventory")

    def is_borrowable(self):
        return self.count - self.borrowed_count > 0

    def is_returnable(self):
        return self.borrowed_count > 0
