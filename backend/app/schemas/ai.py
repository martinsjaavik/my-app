from pydantic import BaseModel


class HintRequest(BaseModel):
    session_id: str
    remaining_words: list[str]


class HintResponse(BaseModel):
    hint: str
    confidence: float
    suggested_words: list[str]


class AutoSolveRequest(BaseModel):
    session_id: str
    remaining_words: list[str]


class AutoSolveStep(BaseModel):
    type: str  # "thinking", "guess", "result"
    content: str
    words: list[str] | None = None
    is_correct: bool | None = None
