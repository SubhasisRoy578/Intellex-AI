from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Float, Integer, Boolean, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base


class Memory(Base):
    """Database model representing personalized long-term facts, preferences, and projects associated with a user."""

    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # preferences, projects, long_term_facts, etc.
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)  # 0.0 (low) to 1.0 (high importance)
    source: Mapped[str] = mapped_column(String(100), default="user", nullable=False)  # user_defined, ai_extracted

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    access_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tags: Mapped[str] = mapped_column(String(255), default="", nullable=False)  # Comma-separated tags, e.g. "python,profile,settings"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)


# Compound indexes to optimize retrieval speed
Index("idx_user_memories_category", Memory.user_id, Memory.category, Memory.is_active)
Index("idx_user_memories_access", Memory.user_id, Memory.last_accessed_at, Memory.is_active)
