from sqlalchemy import Column, Integer, String
from database import Base

class BooksTable(Base):
    __tablename__ = "booksTable"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    rating = Column(Integer)
    published_year = Column(Integer)

