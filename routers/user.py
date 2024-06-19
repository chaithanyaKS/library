from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import SessionLocal
from schemas import user as user_schema
from services import user as user_service


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/users/", response_model=list[user_schema.User])
def get_users(db: Session = Depends(get_db)):
    return user_service.fetch_all(db)


@router.get("/users/{user_id}/", response_model=user_schema.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.post("/users/")
def create_user(user: user_schema.UserCreate, db=Depends(get_db)) -> user_schema.User:
    db_user = user_service.get_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already present"
        )
    return user_service.create(db, user)
