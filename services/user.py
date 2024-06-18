from sqlalchemy.orm import Session

import models


def get_by_id(db: Session, user_id: int):
    return db.query(models.Student).filter(models.Student.id == user_id).first()
