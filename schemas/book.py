from pydantic import BaseModel


class BookBase(BaseModel):
    isbn: str
    title: str
    author: str | None = ""
    subject: str | None = ""


class BookCreate(BookBase):
    pass


class Book(BookBase):
    class Meta:
        orm_mode = True


class BookBorrowReturn(BaseModel):
    isbn: str
