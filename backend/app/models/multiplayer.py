from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class MultiplayerRoom(Base):
    __tablename__ = "multiplayer_rooms"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    room_code: Mapped[str] = mapped_column(String(8), unique=True, index=True)
    puzzle_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("puzzles.id", ondelete="SET NULL"),
        nullable=True,
    )
    host_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(20), default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    max_players: Mapped[int] = mapped_column(Integer, default=4)

    # Relationships
    players = relationship("RoomPlayer", back_populates="room", cascade="all, delete-orphan")


class RoomPlayer(Base):
    __tablename__ = "room_players"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    room_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("multiplayer_rooms.id", ondelete="CASCADE"),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    game_state: Mapped[dict] = mapped_column(JSON, default=dict)
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False)
    finish_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    mistakes: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    room = relationship("MultiplayerRoom", back_populates="players")
