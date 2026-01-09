from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.game import GameSession
from app.models.puzzle import Puzzle, Category
from app.services.puzzle_service import PuzzleService


class GameService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.puzzle_service = PuzzleService(db)

    async def start_game(
        self,
        user_id: str,
        puzzle_id: Optional[str] = None,
        puzzle_date: Optional[str] = None,
    ) -> tuple[GameSession, Puzzle, list[str]]:
        """Start a new game session."""
        # Get puzzle
        if puzzle_id:
            puzzle = await self.puzzle_service.get_puzzle_by_id(puzzle_id)
        elif puzzle_date:
            from datetime import date
            puzzle = await self.puzzle_service.get_puzzle_by_date(
                date.fromisoformat(puzzle_date)
            )
        else:
            puzzle = await self.puzzle_service.get_latest_puzzle()

        if not puzzle:
            raise ValueError("Puzzle not found")

        # Check for existing session
        existing = await self.db.execute(
            select(GameSession)
            .where(
                GameSession.user_id == user_id,
                GameSession.puzzle_id == puzzle.id,
            )
        )
        session = existing.scalar_one_or_none()

        if session:
            # Return existing session
            shuffled_words = self._get_remaining_words(puzzle, session.categories_solved)
        else:
            # Create new session
            session = GameSession(
                user_id=user_id,
                puzzle_id=puzzle.id,
            )
            self.db.add(session)
            await self.db.commit()
            await self.db.refresh(session)
            shuffled_words = self.puzzle_service.get_shuffled_words(puzzle)

        return session, puzzle, shuffled_words

    async def submit_guess(
        self,
        session_id: str,
        user_id: str,
        words: list[str],
    ) -> tuple[str, Optional[Category], bool, GameSession]:
        """
        Submit a guess and return result.
        Returns: (result, category_if_correct, one_away, updated_session)
        """
        # Get session
        result = await self.db.execute(
            select(GameSession)
            .where(
                GameSession.id == session_id,
                GameSession.user_id == user_id,
            )
            .options(selectinload(GameSession.puzzle).selectinload(Puzzle.categories))
        )
        session = result.scalar_one_or_none()

        if not session:
            raise ValueError("Game session not found")

        if session.completed_at:
            raise ValueError("Game already completed")

        # Check if guess is correct
        correct_category = None
        for category in session.puzzle.categories:
            if set(category.words) == set(words):
                correct_category = category
                break

        # Check for "one away" (3 of 4 words correct)
        one_away = False
        if not correct_category:
            for category in session.puzzle.categories:
                matching = len(set(category.words) & set(words))
                if matching == 3:
                    one_away = True
                    break

        # Update session
        guesses = session.guesses or []
        guesses.append({
            "words": words,
            "result": "correct" if correct_category else "wrong",
            "one_away": one_away if not correct_category else None,
        })
        session.guesses = guesses

        if correct_category:
            # Correct guess
            solved = session.categories_solved or []
            solved.append({
                "id": correct_category.id,
                "name": correct_category.name,
                "difficulty": correct_category.difficulty,
                "words": correct_category.words,
                "color": correct_category.color,
            })
            session.categories_solved = solved

            # Check if game is won
            if len(solved) == 4:
                session.completed_at = datetime.utcnow()
                session.is_won = True
                session.solve_time_ms = int(
                    (session.completed_at - session.started_at).total_seconds() * 1000
                )
        else:
            # Wrong guess
            session.mistakes += 1

            # Check if game is lost
            if session.mistakes >= 4:
                session.completed_at = datetime.utcnow()
                session.is_won = False
                session.solve_time_ms = int(
                    (session.completed_at - session.started_at).total_seconds() * 1000
                )

        await self.db.commit()
        await self.db.refresh(session)

        return (
            "correct" if correct_category else "wrong",
            correct_category,
            one_away,
            session,
        )

    async def mark_hint_used(self, session_id: str, user_id: str) -> None:
        """Mark that AI hint was used in session."""
        result = await self.db.execute(
            select(GameSession)
            .where(
                GameSession.id == session_id,
                GameSession.user_id == user_id,
            )
        )
        session = result.scalar_one_or_none()

        if session:
            session.used_ai_hint = True
            await self.db.commit()

    def _get_remaining_words(
        self,
        puzzle: Puzzle,
        solved_categories: list[dict],
    ) -> list[str]:
        """Get words not yet solved."""
        import random

        solved_words = set()
        for cat in solved_categories:
            solved_words.update(cat.get("words", []))

        remaining = []
        for category in puzzle.categories:
            for word in category.words:
                if word not in solved_words:
                    remaining.append(word)

        random.shuffle(remaining)
        return remaining

    async def get_session(self, session_id: str) -> Optional[GameSession]:
        """Get a game session by ID."""
        result = await self.db.execute(
            select(GameSession)
            .where(GameSession.id == session_id)
            .options(selectinload(GameSession.puzzle).selectinload(Puzzle.categories))
        )
        return result.scalar_one_or_none()
