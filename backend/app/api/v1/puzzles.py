from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.puzzle_service import PuzzleService
from app.schemas.puzzle import PuzzleResponse

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.get("/today", response_model=PuzzleResponse)
async def get_todays_puzzle(
    db: AsyncSession = Depends(get_db),
):
    """Get today's puzzle."""
    service = PuzzleService(db)
    puzzle = await service.get_latest_puzzle()

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No puzzle available for today",
        )

    return PuzzleResponse(
        id=puzzle.id,
        puzzle_number=puzzle.puzzle_number,
        date=puzzle.date,
        words=service.get_shuffled_words(puzzle),
    )


@router.get("/archive")
async def get_archive(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Get list of all available puzzles."""
    service = PuzzleService(db)
    puzzles, total = await service.get_archive(limit=limit, offset=offset)

    return {
        "puzzles": [
            {
                "id": p.id,
                "puzzle_number": p.puzzle_number,
                "date": p.date.isoformat(),
            }
            for p in puzzles
        ],
        "total": total,
    }


@router.get("/{puzzle_date}", response_model=PuzzleResponse)
async def get_puzzle_by_date(
    puzzle_date: str,
    db: AsyncSession = Depends(get_db),
):
    """Get puzzle for a specific date (YYYY-MM-DD)."""
    try:
        parsed_date = date.fromisoformat(puzzle_date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD",
        )

    service = PuzzleService(db)
    puzzle = await service.get_puzzle_by_date(parsed_date)

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No puzzle found for {puzzle_date}",
        )

    return PuzzleResponse(
        id=puzzle.id,
        puzzle_number=puzzle.puzzle_number,
        date=puzzle.date,
        words=service.get_shuffled_words(puzzle),
    )


@router.post("/sync")
async def sync_puzzles(
    db: AsyncSession = Depends(get_db),
):
    """Sync puzzles from GitHub source."""
    service = PuzzleService(db)
    count = await service.sync_puzzles_from_github()

    return {
        "message": f"Synced {count} new puzzles",
        "synced_count": count,
    }
