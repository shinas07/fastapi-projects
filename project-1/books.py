from fastapi import FastAPI,HTTPException,status, Path, Query
from pydantic import BaseModel, Field
from typing import Optional



app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: str

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed to create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0,lt=6)
    published_date: int = Field(gt=1900,lt=2038)

    model_config  = {
        "json_schema_extra": {
            "example": {
                "title":"A new book",
                "author": "shinas",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }


BOOKS = [
    Book(1,'Computer Programming Pro', 'Shinas', "A very nice book",5,2030),
    Book(2,'Be Fast with Fastapi', 'Shinas', "A very nice book",5,2030),
    Book(3,'Mastering Endpoints', 'Shinas', "A very nice book",5,2035),
    Book(4,'Bignner guid into Redis', 'Shinas', "A very nice book",5,2033),
    Book(5,'Dive Deeper into system desgining', 'Shinas', "A very nice book",5,2034),
    Book(6,'Learn how to code', 'Shinas', "A very nice book",5,2025),

]

@app.get("/get-books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404,detail='item not found')


@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/",status_code=status.HTTP_200_OK)
async def read_book_by_publish(published_date: int = Query(gt=1999, lt=2038)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return True



def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book



@app.put("/books/update-book", status_code=status.HTTP_200_OK)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='item not found')
    



@app.delete('/books/delete-book/{book_title}',status_code=status.HTTP_200_OK)
async def delete_books(book_title : str):
    book_title = book_title.casefold()
    
    for book in BOOKS:
        if book.get('title','').casefold() == book_title:
            BOOKS.remove(book)
            return {"message":f"Book '{book_title}' deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with title '{book_title}' not found."

    )



            
            
