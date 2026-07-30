from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from app.config.config import settings

# Initialize modern async SQLAlchemy engine
# pool_pre_ping checks connections are alive before serving them
engine: AsyncEngine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    future=True,
)


class Base(DeclarativeBase):
    """Declarative base class for all application SQLAlchemy models."""
    pass
