from sqlalchemy.orm import Session

import models
from schemas.book import BookCreate


def fetch_by_isbn(db: Session, isbn: str) -> models.Book | None:
    return db.query(models.Book).get({"isbn": isbn})


def fetch_all(db: Session) -> list[models.Book]:
    return db.query(models.Book).all()


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
