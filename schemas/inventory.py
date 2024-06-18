from pydantic import BaseModel, PositiveInt


class InventoryBook(BaseModel):
    isbn: str
    title: str


class InventoryBase(BaseModel):
    count: PositiveInt
    book: InventoryBook


class Inventory(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    count: PositiveInt
