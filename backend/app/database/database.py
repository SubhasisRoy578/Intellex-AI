from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from app.config.config import settings

# Initialize modern async SQLAlchemy engine with production pooling optimizations
engine: AsyncEngine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=1800,  # Recycle connections after 30 minutes to prevent stales
    pool_pre_ping=True,  # Guard check connection matches before transactions
    future=True,
)


class Base(DeclarativeBase):
    """Declarative base class for all application SQLAlchemy models."""
    pass
