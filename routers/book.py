from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas import book as book_schema
from services import book as book_service

router = APIRouter(prefix="/books")


@router.get("/", response_model=list[book_schema.Book])
def get_all_books(db: Session = Depends(get_db)):
    books = book_service.fetch_all(db)
    return books


@router.post("/", response_model=book_schema.Book)
def create(book: book_schema.BookCreate, db: Session = Depends(get_db)):
    print("in router", book)
    db_book = book_service.fetch_by_isbn(db, book.isbn)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"book with the isbn {book.isbn} already exists",
        )
    db_book = book_service.create_book(db, book)
    return db_book


@router.get("/{isbn}/")
def get_book(isbn: str, db: Session = Depends(get_db)) -> book_schema.Book:
    book = book_service.fetch_by_isbn(db, isbn)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid isbn {isbn}"
        )
    return book


@router.post("/borrow/")
def borrow(books: book_schema.BookBorrowReturn, db: Session = Depends(get_db)):
    if len(books.isbns) > 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only borrow 3 books at a time",
        )
    user_id = 1
    try:
        book_service.borrow(db, books, user_id)
        return {"detail": "borrowing successful"}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="cannot borrow same book"
        )


@router.post("/return/")
def return_book(books: book_schema.BookBorrowReturn, db: Session = Depends(get_db)):
    if len(books.isbns) > 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only borrow 3 books at a time",
        )
    user_id = 1
    book_service.return_book(db, books, user_id)
    return {"detail": "returning successful"}
