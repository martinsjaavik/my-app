import random
from datetime import date, datetime
from typing import Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.puzzle import Puzzle, Category

# Difficulty color mapping
DIFFICULTY_COLORS = {
    0: "yellow",
    1: "green",
    2: "blue",
    3: "purple",
}


class PuzzleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sync_puzzles_from_github(self) -> int:
        """Fetch all puzzles from GitHub and sync to database."""
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.puzzle_source_url)
            response.raise_for_status()
            puzzles_data = response.json()

        synced_count = 0
        for puzzle_data in puzzles_data:
            existing = await self.get_puzzle_by_number(puzzle_data["id"])
            if not existing:
                await self._create_puzzle(puzzle_data)
                synced_count += 1

        await self.db.commit()
        return synced_count

    async def _create_puzzle(self, puzzle_data: dict) -> Puzzle:
        """Create a puzzle from GitHub JSON data."""
        # Parse date from puzzle data
        # The GitHub data has format like "2024-01-15"
        puzzle_date = date.fromisoformat(puzzle_data.get("date", "2024-01-01"))

        puzzle = Puzzle(
            puzzle_number=puzzle_data["id"],
            date=puzzle_date,
            source_url=settings.puzzle_source_url,
        )
        self.db.add(puzzle)
        await self.db.flush()

        # Create categories
        for i, group in enumerate(puzzle_data.get("answers", [])):
            category = Category(
                puzzle_id=puzzle.id,
                name=group.get("group", f"Category {i+1}"),
                difficulty=group.get("level", i),
                words=group.get("members", []),
                color=DIFFICULTY_COLORS.get(group.get("level", i), "yellow"),
            )
            self.db.add(category)

        return puzzle

    async def get_todays_puzzle(self) -> Optional[Puzzle]:
        """Get today's puzzle."""
        today = date.today()
        return await self.get_puzzle_by_date(today)

    async def get_puzzle_by_date(self, puzzle_date: date) -> Optional[Puzzle]:
        """Get puzzle for a specific date."""
        result = await self.db.execute(
            select(Puzzle)
            .where(Puzzle.date == puzzle_date)
            .options(selectinload(Puzzle.categories))
        )
        return result.scalar_one_or_none()

    async def get_puzzle_by_number(self, puzzle_number: int) -> Optional[Puzzle]:
        """Get puzzle by puzzle number."""
        result = await self.db.execute(
            select(Puzzle)
            .where(Puzzle.puzzle_number == puzzle_number)
            .options(selectinload(Puzzle.categories))
        )
        return result.scalar_one_or_none()

    async def get_puzzle_by_id(self, puzzle_id: str) -> Optional[Puzzle]:
        """Get puzzle by ID."""
        result = await self.db.execute(
            select(Puzzle)
            .where(Puzzle.id == puzzle_id)
            .options(selectinload(Puzzle.categories))
        )
        return result.scalar_one_or_none()

    async def get_latest_puzzle(self) -> Optional[Puzzle]:
        """Get the most recent puzzle."""
        result = await self.db.execute(
            select(Puzzle)
            .order_by(Puzzle.date.desc())
            .limit(1)
            .options(selectinload(Puzzle.categories))
        )
        return result.scalar_one_or_none()

    async def get_archive(self, limit: int = 50, offset: int = 0) -> tuple[list[Puzzle], int]:
        """Get list of all puzzles for archive."""
        # Get total count
        count_result = await self.db.execute(
            select(Puzzle.id)
        )
        total = len(count_result.all())

        # Get puzzles
        result = await self.db.execute(
            select(Puzzle)
            .order_by(Puzzle.date.desc())
            .limit(limit)
            .offset(offset)
        )
        puzzles = result.scalars().all()

        return list(puzzles), total

    def get_shuffled_words(self, puzzle: Puzzle) -> list[str]:
        """Get all words from puzzle categories, shuffled."""
        all_words = []
        for category in puzzle.categories:
            all_words.extend(category.words)
        random.shuffle(all_words)
        return all_words
