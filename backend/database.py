import hashlib
from uuid import uuid4

from sqlalchemy import create_engine
from backend.tables import Book, Exercises, Summary


class DatabaseInterface:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.conn = self.engine.connect()

    def add_book(self, book_path: str):
        book_hash = hashlib.sha256(str(uuid4()).encode()).hexdigest()
        book = Book(book_hash=book_hash, path=book_path)
        self.conn.execute(book.insert())
        return True
    
    def add_exercise(self, book_hash: str, exercise: str, page: int, question: str, answer: str):
        exercise = Exercises(book_hash=book_hash, exercise=exercise, page=page, question=question, answer=answer)
        self.conn.execute(exercise.insert())
        return True
        
    def add_summary(self, book_hash: str, page: int, summary: str):
        summary = Summary(book_hash=book_hash, page=page, summary=summary)
        self.conn.execute(summary.insert())
        return True
    
    def get_book_path(self, book_hash: str):
        query = Book.select().where(Book.c.book_hash == book_hash)
        result = self.conn.execute(query)
        row = result.fetchone()
        return row["path"]
    
    def get_exercises(self, book_hash: str):
        query = Exercises.select().where(Exercises.c.book_hash == book_hash)
        result = self.conn.execute(query)
        return result.fetchall()
    
    def get_summary(self, book_hash: str, page):
        query = Summary.select().where(Summary.c.book_hash == book_hash and Summary.c.page == page)
        result = self.conn.execute(query)
        return result.fetchall()

    