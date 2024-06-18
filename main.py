from fastapi import FastAPI

from routers import book, inventory, user

app = FastAPI()


@app.get("/ping")
def ping():
    return {"detail": "Service up and running"}


app.include_router(user.router, prefix="/api/v1")
app.include_router(book.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
