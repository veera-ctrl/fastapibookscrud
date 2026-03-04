from fastapi import FastAPI,Body
from pydantic import BaseModel,Field


app=FastAPI()

class Book:
    id:int
    title:str
    description:str
    author:str
    rating:int

    def __init__(self,id,title,description,author,rating):
        self.id=id
        self.title=title
        self.description=description
        self.author=author
        self.rating=rating


class BookRequest(BaseModel):
    id:int
    title:str=Field(min_length=3)   
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1,lt=6)
    
 
BOOKS=[Book(1,"Title One","Description One","Author One",5),
       Book(2,"Title Two","Description Two","Author Two",4),
       Book(3,"Title Three","Description Three","Author Three",3),
       Book(4,"Title Four","Description Four","Author Four",2)]

@app.get("/books/")

def read_All_books():
    return BOOKS


@app.get("/books/{book_id}")
def read_book(book_id:int):
    for book in BOOKS:
        if book.id==book_id:
            return book



@app.get("/books/")
def read_book_by_rating(book_rating:int):
    books_to_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
def create_book(book_request:BookRequest):
    print(type(book_request))
    new_book=Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book)
    )

@app.delete("/books/{book_id}")
def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break


def find_book_id(book=Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book

    