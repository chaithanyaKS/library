from pydantic import BaseModel, PositiveInt


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
    isbns: list[str]
