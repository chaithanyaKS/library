from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from db import SessionLocal, TestingSessionLocal
from services import user as user_service

security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    db = next(get_db())
    user = user_service.get_by_email(db, credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    if not user.check_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    return user.email
