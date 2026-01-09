from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.core.database import get_db
from app.core.security import require_user
from app.services.ai_service import ai_service
from app.services.game_service import GameService
from app.schemas.ai import HintRequest, HintResponse, AutoSolveRequest

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/hint", response_model=HintResponse)
async def get_hint(
    request: HintRequest,
    user_id: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Get an AI hint for the current game state."""
    # Verify session belongs to user
    service = GameService(db)
    session = await service.get_session(request.session_id)

    if not session or session.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found",
        )

    if session.completed_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game already completed",
        )

    # Mark hint as used
    await service.mark_hint_used(request.session_id, user_id)

    # Get hint from AI
    solved_count = len(session.categories_solved or [])
    hint = await ai_service.get_hint(
        remaining_words=request.remaining_words,
        solved_count=solved_count,
    )

    return HintResponse(
        hint=hint["hint"],
        confidence=hint["confidence"],
        suggested_words=hint["suggested_words"],
    )


@router.post("/solve")
async def start_auto_solve(
    request: AutoSolveRequest,
    user_id: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Start AI auto-solve and stream the results."""
    # Verify session belongs to user
    service = GameService(db)
    session = await service.get_session(request.session_id)

    if not session or session.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found",
        )

    async def generate():
        mistakes_remaining = 4 - session.mistakes
        solved_categories = session.categories_solved or []

        async for step in ai_service.auto_solve_step(
            remaining_words=request.remaining_words,
            mistakes_remaining=mistakes_remaining,
            solved_categories=solved_categories,
        ):
            yield f"data: {json.dumps(step)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
