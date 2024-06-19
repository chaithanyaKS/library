from sqlalchemy.orm import Session

import models
from schemas import user as user_schema


def fetch_all(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def get_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create(db: Session, user: user_schema.UserCreate) -> models.User:
    user = models.User(
        email=user.email,
        name=user.name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        password=user.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
