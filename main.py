from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasicCredentials

from dependencies import authenticate_user
from routers import book, inventory, user

app = FastAPI()


@app.get("/ping")
def ping(
    credentials: Annotated[HTTPBasicCredentials, Depends(authenticate_user)],
):
    return {"detail": "Service up and running"}


app.include_router(user.router, prefix="/api/v1")
app.include_router(book.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
