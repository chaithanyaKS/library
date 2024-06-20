from fastapi import status
from fastapi.testclient import TestClient

from db import Base, testing_engine
from main import app


def setup_function(function):
    Base.metadata.create_all(bind=testing_engine)


client = TestClient(app)


def test_fetch_book_by_isbn(book):
    endpoint = f"/api/v1/books/{book.isbn}/"
    res = client.get(endpoint)

    assert res.status_code == status.HTTP_200_OK


def test_add_book(auth_header):
    endpoint = "/api/v1/books/"
    body = {"title": "some book", "isbn": "2"}
    print(auth_header)

    res1 = client.get("/api/v1/users/1/")
    data = res1.json()
    print(data)

    res = client.post(endpoint, json=body, headers=auth_header)
    print(res.headers)

    assert res.status_code == status.HTTP_201_CREATED
