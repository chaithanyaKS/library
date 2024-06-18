from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from routers.user import get_db
from schemas import inventory as inventory_schema
from services import inventory as inventory_service

router = APIRouter(prefix="/inventory")


@router.get("/", response_model=list[inventory_schema.Inventory])
def get_inventory(db: Session = Depends(get_db)):
    return inventory_service.fetch_all(db)


@router.patch("/{isbn}", response_model=inventory_schema.Inventory)
def update_count(
    isbn: str,
    inventory: inventory_schema.InventoryUpdate,
    db: Session = Depends(get_db),
):
    try:
        db_inventory = inventory_service.update_inventory(db, isbn, inventory.count)
        return db_inventory
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"isbn {isbn} does not exist"
        )