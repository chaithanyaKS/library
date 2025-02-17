from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from dependencies import authenticate_user, get_db
from exceptions import (
    BookNotAvaibaleError,
    BookNotReturnableError,
    BorrowingExceededError,
)
from schemas import book as book_schema
from services import book as book_service

router = APIRouter(prefix="/books", tags=["book"])


@router.get("/", response_model=list[book_schema.Book])
def get_all_books(db: Session = Depends(get_db)):
    books = book_service.fetch_all(db)
    return books


@router.post("/", response_model=book_schema.Book, status_code=status.HTTP_201_CREATED)
def create(
    credentials: Annotated[HTTPBasicCredentials, Depends(authenticate_user)],
    book: book_schema.BookCreate,
    db: Session = Depends(get_db),
):
    try:
        db_book = book_service.fetch_by_isbn(db, book.isbn)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"book with the isbn {book.isbn} already exists",
        )
    except NoResultFound:
        db_book = book_service.create_book(db, book)
        return db_book


@router.get("/popular/", response_model=list[book_schema.Book])
def get_popular_books(db: Session = Depends(get_db)):
    popular_books = book_service.popular(db)

    return popular_books


@router.get("/{isbn}/")
def get_book(isbn: str, db: Session = Depends(get_db)) -> book_schema.Book:
    try:
        book = book_service.fetch_by_isbn(db, isbn)
        return book
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid isbn {isbn}"
        )


@router.post("/borrow/")
def borrow(
    email: Annotated[HTTPBasicCredentials, Depends(authenticate_user)],
    book: book_schema.BookBorrowReturn,
    db: Session = Depends(get_db),
):
    try:
        book_service.borrow(db, book, email)
        return {"detail": "borrowing successful"}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="cannot borrow same book"
        )
    except BookNotAvaibaleError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="book not available for borrowing",
        )
    except BorrowingExceededError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only 3 books can be borrowed",
        )


@router.post("/return/")
def return_book(
    email: Annotated[HTTPBasicCredentials, Depends(authenticate_user)],
    book: book_schema.BookBorrowReturn,
    db: Session = Depends(get_db),
):
    try:
        book_service.return_book(db, book)
        return {"detail": "returning successful"}
    except BookNotReturnableError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book not returnable",
        )
