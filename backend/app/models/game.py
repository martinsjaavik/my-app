from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    puzzle_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("puzzles.id", ondelete="CASCADE"),
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    mistakes: Mapped[int] = mapped_column(Integer, default=0)
    solve_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    guesses: Mapped[dict] = mapped_column(JSON, default=list)
    categories_solved: Mapped[dict] = mapped_column(JSON, default=list)
    is_won: Mapped[bool] = mapped_column(Boolean, nullable=True)
    used_ai_hint: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="game_sessions")
    puzzle = relationship("Puzzle", back_populates="game_sessions")
