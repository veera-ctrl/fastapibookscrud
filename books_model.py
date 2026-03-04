from fastapi import FastAPI,Body
from pydantic import BaseModel,Field
from typing import Optional


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
    id:Optional[int]=None
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

@app.post("/create-book")
def create_book(book_request:BookRequest):
   
    new_book = Book(**book_request.dict())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)
    return {"status": "created", "book": new_book}

def find_book_id(book=Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book