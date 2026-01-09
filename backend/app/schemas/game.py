from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.puzzle import PuzzleResponse, CategoryResponse


class GuessResult(BaseModel):
    words: list[str]
    result: str  # "correct" or "wrong"
    one_away: Optional[bool] = None
    category: Optional[CategoryResponse] = None


class GameStateResponse(BaseModel):
    remaining_words: list[str]
    solved_categories: list[CategoryResponse]
    mistakes: int
    guesses: list[GuessResult]
    is_complete: bool
    is_won: Optional[bool] = None
    solve_time_ms: Optional[int] = None


class GameStartRequest(BaseModel):
    puzzle_id: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD format


class GameStartResponse(BaseModel):
    session_id: str
    puzzle: PuzzleResponse
    game_state: GameStateResponse


class GuessRequest(BaseModel):
    words: list[str]


class GuessResponse(BaseModel):
    result: str  # "correct" or "wrong"
    one_away: Optional[bool] = None
    category: Optional[CategoryResponse] = None
    game_state: GameStateResponse
