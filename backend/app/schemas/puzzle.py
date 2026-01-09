from pydantic import BaseModel
from datetime import date
from typing import Optional


class CategoryResponse(BaseModel):
    id: str
    name: str
    difficulty: int
    words: list[str]
    color: str

    class Config:
        from_attributes = True


class PuzzleResponse(BaseModel):
    id: str
    puzzle_number: int
    date: date
    words: list[str]  # Shuffled words for gameplay

    class Config:
        from_attributes = True


class PuzzleWithCategoriesResponse(PuzzleResponse):
    categories: list[CategoryResponse]
