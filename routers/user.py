from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import SessionLocal
from schemas import user as user_schema
from services import user as user_model


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/user/{user_id}/", response_model=user_schema.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_model.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
