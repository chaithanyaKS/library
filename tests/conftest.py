import base64

import pytest

from dependencies import get_test_db
from models import Book, User


@pytest.fixture
def users():
    db = next(get_test_db())
    users = [
        {
            "name": "test1",
            "email": "test1@test.com",
            "password": "test@123",
        },
        {
            "name": "test2",
            "email": "test2@test.com",
            "password": "test@123",
        },
        {
            "name": "test3",
            "email": "test3@test.com",
            "password": "test@123",
        },
        {
            "name": "test3",
            "email": "test4@test.com",
            "password": "test@123",
        },
    ]
    users = [
        User(name=user["name"], email=user["email"], password=user["password"])
        for user in users
    ]
    db.add_all(users)


@pytest.fixture
def user():
    db = next(get_test_db())
    user_dict = {
        "name": "test1",
        "email": "test1@test.com",
        "password": "test@123",
    }
    user = User(
        name=user_dict["name"], email=user_dict["email"], password=user_dict["password"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user

    db.delete(user)


@pytest.fixture
def book():
    db = next(get_test_db())
    book = Book(isbn="1", title="some book", author="", subject="")
    db.add(book)
    db.commit()
    db.refresh(book)
    yield book
    db.delete(book)
    db.commit()


@pytest.fixture()
def token(user):
    return base64.b64encode(bytes(f"{user.email}:test@123", "utf-8")).decode("ascii")


@pytest.fixture
def auth_header(token):
    return {"Authorization": f"Basic {token}"}
