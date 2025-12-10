from fastapi import Body, FastAPI

# Create the FastAPI application instance
app = FastAPI()

# In-memory "database" of books (a simple Python list of dicts)
BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author One", "category": "math"},
]


# ==============================
# Get all books
# ==============================
@app.get("/books")
async def read_all_books():
    """Return the full list of books."""
    return BOOKS


# ==============================
# Get a single book by title (path)
# ==============================
@app.get("/books/title/{book_title}")
async def read_book(book_title: str):
    """Find a book by title."""
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    return {"error": "Book not found"}


# ==============================
# Get books by author AND category
# ==============================
@app.get("/books/author/{book_author}")
async def read_author_and_category(book_author: str, category: str):
    """Filter books by both author and category."""
    books_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == book_author.casefold()
            and book.get('category').casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# ==============================
# Query param version
# ==============================
@app.get("/books/specific/author")
async def read_specific_book_author(author: str):
    """Filter books by author (query param)."""
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


# ==============================
# Path param version
# ==============================
@app.get("/books/specific/author/{author}")
async def read_specific_book_author(author: str):
    """Filter books by author (path)."""
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


# ==============================
# Create a new book
# ==============================
@app.post("/books/create")
async def create_book(new_book=Body()):
    """Add a new book to the BOOKS list."""
    BOOKS.append(new_book)


# ==============================
# Update existing book
# ==============================
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    """Update a book based on matching title."""
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


# ==============================
# Delete a book
# ==============================
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    """Delete a book by title."""
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break



"""
===========================================================
README 
===========================================================

📚 FastAPI Books API

A simple FastAPI project to practice:
- GET
- POST
- PUT
- DELETE
- Path parameters
- Query parameters
- Request body (Body())

------------------------------------
🚀 Run the API
------------------------------------
uvicorn books:app --reload

Open your browser:
http://127.0.0.1:8000/docs

------------------------------------
🔎 Endpoints
------------------------------------

GET /books
    Get all books

GET /books/title/{book_title}
    Find a book by title (path parameter)

GET /books/author/{author}?category=math
    Find by author AND category

GET /books/specific/author?author=Author One
    Query parameter

GET /books/specific/author/{author}
    Path parameter

POST /books/create
    Create new book
    Body example:
    {
        "title": "My Title",
        "author": "Me",
        "category": "history"
    }

PUT /books/update_book
    Update by title

DELETE /books/delete_book/{book_title}
    Delete book

------------------------------------
This project is only for learning purposes.
In a real case, a database would be used.
===========================================================
END README
===========================================================
"""
