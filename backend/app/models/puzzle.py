from datetime import datetime, date
from uuid import uuid4

from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Puzzle(Base):
    __tablename__ = "puzzles"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    puzzle_number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    date: Mapped[date] = mapped_column(Date, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    source_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Relationships
    categories = relationship("Category", back_populates="puzzle", cascade="all, delete-orphan")
    game_sessions = relationship("GameSession", back_populates="puzzle")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    puzzle_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("puzzles.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100))
    difficulty: Mapped[int] = mapped_column(Integer)  # 0=Yellow, 1=Green, 2=Blue, 3=Purple
    words: Mapped[list[str]] = mapped_column(ARRAY(String))
    color: Mapped[str] = mapped_column(String(20))

    # Relationships
    puzzle = relationship("Puzzle", back_populates="categories")
