from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas import user as user_schema
from services import user as user_service

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/", response_model=list[user_schema.User])
def get_users(db: Session = Depends(get_db)):
    return user_service.fetch_all(db)


@router.get("/{user_id}/", response_model=user_schema.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db=Depends(get_db)) -> user_schema.User:
    db_user = user_service.get_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already present"
        )
    return user_service.create(db, user)
