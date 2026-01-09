from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_user
from app.services.game_service import GameService
from app.services.puzzle_service import PuzzleService
from app.schemas.game import (
    GameStartRequest,
    GameStartResponse,
    GuessRequest,
    GuessResponse,
    GameStateResponse,
    GuessResult,
)
from app.schemas.puzzle import PuzzleResponse, CategoryResponse

router = APIRouter(prefix="/games", tags=["games"])


def _build_game_state(session, puzzle) -> GameStateResponse:
    """Build game state response from session."""
    # Get remaining words
    solved_words = set()
    for cat in session.categories_solved or []:
        solved_words.update(cat.get("words", []))

    remaining = []
    for category in puzzle.categories:
        for word in category.words:
            if word not in solved_words:
                remaining.append(word)

    return GameStateResponse(
        remaining_words=remaining,
        solved_categories=[
            CategoryResponse(
                id=cat["id"],
                name=cat["name"],
                difficulty=cat["difficulty"],
                words=cat["words"],
                color=cat["color"],
            )
            for cat in (session.categories_solved or [])
        ],
        mistakes=session.mistakes,
        guesses=[
            GuessResult(
                words=g["words"],
                result=g["result"],
                one_away=g.get("one_away"),
            )
            for g in (session.guesses or [])
        ],
        is_complete=session.completed_at is not None,
        is_won=session.is_won,
        solve_time_ms=session.solve_time_ms,
    )


@router.post("", response_model=GameStartResponse)
async def start_game(
    request: GameStartRequest,
    user_id: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Start a new game session."""
    service = GameService(db)

    try:
        session, puzzle, words = await service.start_game(
            user_id=user_id,
            puzzle_id=request.puzzle_id,
            puzzle_date=request.date,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return GameStartResponse(
        session_id=session.id,
        puzzle=PuzzleResponse(
            id=puzzle.id,
            puzzle_number=puzzle.puzzle_number,
            date=puzzle.date,
            words=words,
        ),
        game_state=_build_game_state(session, puzzle),
    )


@router.patch("/{session_id}/guess", response_model=GuessResponse)
async def submit_guess(
    session_id: str,
    request: GuessRequest,
    user_id: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a guess (4 words)."""
    if len(request.words) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must submit exactly 4 words",
        )

    service = GameService(db)

    try:
        result, category, one_away, session = await service.submit_guess(
            session_id=session_id,
            user_id=user_id,
            words=request.words,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # Get puzzle for remaining words calculation
    puzzle_service = PuzzleService(db)
    puzzle = await puzzle_service.get_puzzle_by_id(session.puzzle_id)

    return GuessResponse(
        result=result,
        one_away=one_away if result == "wrong" else None,
        category=CategoryResponse.model_validate(category) if category else None,
        game_state=_build_game_state(session, puzzle),
    )


@router.get("/{session_id}")
async def get_game_session(
    session_id: str,
    user_id: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Get game session details."""
    service = GameService(db)
    session = await service.get_session(session_id)

    if not session or session.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found",
        )

    puzzle_service = PuzzleService(db)
    puzzle = await puzzle_service.get_puzzle_by_id(session.puzzle_id)

    return {
        "session_id": session.id,
        "puzzle": {
            "id": puzzle.id,
            "puzzle_number": puzzle.puzzle_number,
            "date": puzzle.date.isoformat(),
        },
        "game_state": _build_game_state(session, puzzle),
    }


@router.get("/history")
async def get_game_history(
    limit: int = 20,
    user_id: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's game history."""
    from sqlalchemy import select
    from app.models.game import GameSession
    from sqlalchemy.orm import selectinload

    result = await db.execute(
        select(GameSession)
        .where(
            GameSession.user_id == user_id,
            GameSession.completed_at.isnot(None),
        )
        .order_by(GameSession.completed_at.desc())
        .limit(limit)
        .options(selectinload(GameSession.puzzle))
    )
    sessions = result.scalars().all()

    return {
        "games": [
            {
                "session_id": s.id,
                "puzzle": {
                    "id": s.puzzle.id,
                    "puzzle_number": s.puzzle.puzzle_number,
                    "date": s.puzzle.date.isoformat(),
                },
                "is_won": s.is_won,
                "mistakes": s.mistakes,
                "solve_time_ms": s.solve_time_ms,
                "completed_at": s.completed_at.isoformat() if s.completed_at else None,
            }
            for s in sessions
        ]
    }
