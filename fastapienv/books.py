from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author One", "category": "math"},
]


# Get all books
@app.get("/books")
async def read_all_books():
    return BOOKS


# Get a book by title
@app.get("/books/title/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    return {"error": "Book not found"}


# Get books by author and category
@app.get("/books/author/{book_author}")
async def read_author_and_category(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == book_author.casefold()
            and book.get('category').casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return



# query params
@app.get("/books/specific/author")
async def read_specific_book_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return



# path params
@app.get("/books/specific/author/{author}")
async def read_specific_book_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return




# Create a new book
@app.post("/books/create")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


