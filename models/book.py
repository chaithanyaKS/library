from sqlalchemy import ForeignKey, UniqueConstraint
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


class Borrowing(Base):
    __tablename__ = "borrowing"
    id: Mapped[int] = mapped_column(primary_key=True)
    inventory_id: Mapped[str] = mapped_column(ForeignKey(column="inventory.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey(column="user_account.id"))
    __table_args__ = (
        UniqueConstraint("inventory_id", "user_id", name="uniq_inventory_id_user_id"),
    )
