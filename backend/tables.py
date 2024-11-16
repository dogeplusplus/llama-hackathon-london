from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    book_hash = Column(String, primary_key=True)
    path = Column(String)


class Summary(Base):
    __tablename__ = "summary"
    book_hash = Column(String, primary_key=True)
    page = Column(Integer)
    summary = Column(String)


class Exercises(Base):
    __tablename__ = "exercises"
    book_hash = Column(String, primary_key=True)
    page = Column(Integer)
    question = Column(String)
    answer = Column(String)
