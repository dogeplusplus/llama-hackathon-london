from typing import Optional
from pydantic import BaseModel


class Question(BaseModel):
    book_hash: str
    page: str
    question: Optional[str]
    highlighted_text: Optional[str]


class Summarize(BaseModel):
    book_hash: str
    page: str


class Exercises(BaseModel):
    book_hash: str
    page: int

