from typing import Optional

from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1,max_length=100)
    rating: int = Field(gt=0,lt=6)
    published_date: int = Field(gte=1900,lte=2100)


    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2025
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5,2000),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5,2001),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5,2002),
    Book(4, "HP1", "Author 1", "Book Description", 2,2003),
    Book(5, "HP2", "Author 2", "Book Description", 3,2000),
    Book(6, "HP3", "Author 3", "Book Description", 1,2000),

]


@app.get("/books" , status_code=status.HTTP_200_OK)
async def readAllBooks():
    return BOOKS

@app.get("/books/{id}" , status_code=status.HTTP_200_OK)
async def readBook(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/" , status_code=status.HTTP_200_OK)
async def readBookByRating(bookRating: int = Query(gt=0,lt=6) ):
    booksToReturn = []
    for book in BOOKS:
        if book.rating == bookRating:
            booksToReturn.append(book)
    return booksToReturn


@app.get("/books/published_date/" ,status_code=status.HTTP_200_OK)
async def readBookPublishedDate(published_date: int = Query(gte=1900,lte=2100)):
    booksToReturn = []
    for book in BOOKS:
        if book.published_date == published_date:
            booksToReturn.append(book)
    return booksToReturn


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def createBook(book: BookRequest):
    newBook = Book(**book.dict())
    BOOKS.append(findBookId(newBook))


@app.put("/books/id" , status_code=status.HTTP_204_NO_CONTENT)
async def updateBook( book: BookRequest):
    bookChanged = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            bookChanged = True
    if not bookChanged:
     raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteBook(id: int = Path(gt=0)):
    bookChanged = False
    for book in BOOKS:
        if book.id == id:
            BOOKS.remove(book)
            bookChanged = True
            break
    if not bookChanged:
        raise HTTPException(status_code=404, detail="Book not found")




def findBookId(book: Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    return book



















