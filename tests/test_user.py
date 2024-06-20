from fastapi import status
from fastapi.testclient import TestClient

from db import Base, testing_engine
from dependencies import get_db, get_test_db
from main import app

client = TestClient(app)


def setup_function(function):
    Base.metadata.create_all(bind=testing_engine)


app.dependency_overrides[get_db] = get_test_db


def test_ping():
    res = client.get("/ping/")

    assert res.status_code == status.HTTP_200_OK


def test_create_user():
    body = {
        "name": "test3",
        "email": "test4@test.com",
        "password": "test@123",
    }
    res = client.post("/api/v1/users/", json=body)
    data = res.json()
    assert res.status_code == status.HTTP_201_CREATED
    assert "email" in data
    assert "name" in data
    assert "password" not in data


def test_duplicate_users():
    body1 = {
        "name": "test3",
        "email": "test4@test.com",
        "password": "test@123",
    }
    body2 = {
        "name": "test3",
        "email": "test4@test.com",
        "password": "test@123",
    }

    res1 = client.post("/api/v1/users/", json=body1)
    res2 = client.post("/api/v1/users/", json=body2)

    assert res2.status_code == status.HTTP_400_BAD_REQUEST


def test_get_user_by_id(user):
    res = client.get(f"/api/v1/users/{user.id}/")
    assert res.status_code == status.HTTP_200_OK


def test_get_user_by_invalid_id():
    res = client.get("/api/v1/users/100/")
    assert res.status_code == status.HTTP_404_NOT_FOUND
