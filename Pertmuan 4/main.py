from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
data = []


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str


@app.post("/books")
def add_book(book: Book):
    data.append(book.dict())
    return data


@app.get("/books")
async def get_books():
    return data


@app.get("/books/{id}")
async def get_book(id: int):
    id = id - 1
    return data[id]


@app.put("/books/{id}")
async def add_book(id: int, book: Book):
    data[id - 1] = book
    return data


@app.delete("/book/{id}")
async def delete_book(id: int):
    data.pop(id - 1)
    return data