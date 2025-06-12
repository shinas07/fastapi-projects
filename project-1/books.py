from fastapi import FastAPI,HTTPException,status
from typing import List

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'},
    {'title': 'Title Seven', 'author': 'Author One', 'category': 'history'},

    {'title': 'Title Eight', 'author': 'Author Three', 'category': 'science'}
]

@app.get('/')
async def read_all_books():
    return BOOKS


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



            
            
