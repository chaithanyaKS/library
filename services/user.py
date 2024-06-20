from sqlalchemy.orm import Session

import models as m
from schemas import user as user_schema


def fetch_all(db: Session) -> list[m.User]:
    return db.query(m.User).all()


def get_by_id(db: Session, user_id: int):
    return db.query(m.User).filter(m.User.id == user_id).first()


def get_by_email(db: Session, email: str):
    return db.query(m.User).filter(m.User.email == email).first()


def create(db: Session, user: user_schema.UserCreate) -> m.User:
    user = m.User(
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
