from httpx import delete
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

import models
from models.book import Borrowing
from schemas.book import BookBorrowReturn, BookCreate


def fetch_by_isbn(db: Session, isbn: str) -> models.Book | None:
    return db.query(models.Book).get({"isbn": isbn})


def fetch_all(db: Session) -> list[models.Book]:
    return db.query(models.Book).all()


def borrow(db: Session, books: BookBorrowReturn, email: str):
    user = db.query(models.User).where(models.User.email == email).one()
    count = (
        db.query(func.count(models.Borrowing.user_id))
        .where(models.Borrowing.user_id == user.id)
        .scalar()
    )
    if count >= 3:
        raise Exception("Exceeded borrowing limit")

    borrowings = [Borrowing(book_id=isbn, user_id=user.id) for isbn in books.isbns]
    db.add_all(borrowings)
    db.commit()


def return_book(db: Session, books: BookBorrowReturn, email: str):
    user = db.query(models.User).where(models.User.email == email).one()
    delete(Borrowing).filter(
        Borrowing.book_id.in_(books.isbns),
        Borrowing.user_id == user.id,
    )


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
