from fastapi.security import HTTPBasicCredentials
from sqlalchemy import func
from sqlalchemy.orm import Session

import models as m
from exceptions import (
    BookNotAvaibaleError,
    BookNotReturnableError,
    BorrowingExceededError,
)
from schemas.book import BookBorrowReturn, BookCreate


def fetch_by_isbn(db: Session, isbn: str) -> m.Book | None:
    return db.query(m.Book).filter(m.Book.isbn == isbn).one()


def fetch_all(db: Session) -> list[m.Book]:
    return db.query(m.Book).all()


def borrow(db: Session, book: BookBorrowReturn, email: HTTPBasicCredentials):
    user = db.query(m.User).where(m.User.email == email).one()
    # Check if the user has already borrowed 3 books
    count = (
        db.query(func.count(m.Borrowing.user_id))
        .where(m.Borrowing.user_id == user.id)
        .scalar()
    )
    if count >= 3:
        raise BorrowingExceededError("Exceeded borrowing limit")

    inventory = db.query(m.Inventory).filter(m.Inventory.book_id == book.isbn).scalar()
    # check if there are books to borrow
    if not inventory.is_borrowable():
        raise BookNotAvaibaleError("Book not available")

    inventory.borrowed_count += 1

    borrowing = m.Borrowing(inventory_id=inventory.id, user_id=user.id)
    db.add(borrowing)
    db.add(inventory)
    db.commit()


def return_book(db: Session, book: BookBorrowReturn):
    inventory = db.query(m.Inventory).filter(m.Inventory.book_id == book.isbn).scalar()
    if not inventory.is_returnable():
        raise BookNotReturnableError()

    inventory.borrowed_count -= 1
    db.add(inventory)
    db.commit()


def create_book(db: Session, book: BookCreate) -> m.Book:
    print(book)
    db_book = m.Book(
        isbn=book.isbn,
        title=book.title,
        author=book.author,
        subject=book.subject,
    )
    db_inventory = m.Inventory(count=1, book_id=book.isbn)
    db.add(db_book)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_book)
    return db_book


def popular(db: Session):
    books_q = (
        db.query(m.Book)
        .join(m.Inventory)
        .join(m.Borrowing)
        .group_by(m.Borrowing.inventory_id)
        .order_by(func.count(m.Borrowing.inventory_id).desc())
        .limit(5)
    )
    return books_q
