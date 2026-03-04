
from database import Base,engine

from sqlalchemy import Column,Integer,String,Float

class BooksTable(Base):
    __tabklename__="booksTable"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    author=Column(String)
    rating=Column(Integer)
    published_date=Column(Integer)

        

 
