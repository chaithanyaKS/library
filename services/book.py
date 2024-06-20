from fastapi.security import HTTPBasicCredentials
from httpx import delete
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

import models
from exceptions import BookNotAvaibaleError, BookNotReturnableError
from models.book import Borrowing
from schemas.book import BookBorrowReturn, BookCreate


def fetch_by_isbn(db: Session, isbn: str) -> models.Book | None:
    return db.query(models.Book).filter(models.Book.isbn == isbn).one()


def fetch_all(db: Session) -> list[models.Book]:
    return db.query(models.Book).all()


def borrow(db: Session, book: BookBorrowReturn, email: HTTPBasicCredentials):
    user = db.query(models.User).where(models.User.email == email).one()
    # Check if the user has already borrowed 3 books
    count = (
        db.query(func.count(models.Borrowing.user_id))
        .where(models.Borrowing.user_id == user.id)
        .scalar()
    )
    if count >= 3:
        raise Exception("Exceeded borrowing limit")

    inventory = (
        db.query(models.Inventory)
        .filter(models.Inventory.book_id == book.isbn)
        .scalar()
    )
    # check if there are books to borrow
    if not inventory.is_borrowable():
        raise BookNotAvaibaleError("Book not available")

    inventory.borrowed_count += 1

    borrowing = Borrowing(inventory_id=inventory.id, user_id=user.id)
    db.add(borrowing)
    db.add(inventory)
    db.commit()


def return_book(db: Session, book: BookBorrowReturn, email: HTTPBasicCredentials):
    user = db.query(models.User).where(models.User.email == email).one()

    inventory = (
        db.query(models.Inventory)
        .filter(models.Inventory.book_id == book.isbn)
        .scalar()
    )
    if not inventory.is_returnable():
        raise BookNotReturnableError()

    inventory.borrowed_count -= 1
    borrowing = delete(Borrowing).filter(
        Borrowing.inventory_id == inventory.id,
        Borrowing.user_id == user.id,
    )
    db.add(inventory)
    db.execute(borrowing)
    db.commit()


def create_book(db: Session, book: BookCreate) -> models.Book:
    print(book)
    db_book = models.Book(
        isbn=book.isbn,
        title=book.title,
        author=book.author,
        subject=book.subject,
    )
    db_inventory = models.Inventory(count=1, book_id=book.isbn)
    db.add(db_book)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_book)
    return db_book
