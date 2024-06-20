from sqlalchemy.orm import Session, joinedload

from models import Inventory


def fetch_all(db: Session) -> list[Inventory]:
    db_inventory = db.query(Inventory).options(joinedload(Inventory.book)).all()
    return db_inventory


def update_inventory(db: Session, isbn: str, count: int) -> Inventory:
    db_inventory = db.query(Inventory).filter(Inventory.book_id == isbn).one()
    db_inventory.count = count
    db.commit()
    db.refresh(db_inventory)
    return db_inventory
