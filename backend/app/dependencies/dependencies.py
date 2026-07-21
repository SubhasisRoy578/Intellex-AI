from typing import AsyncGenerator
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_async_db


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to retrieve an asynchronous database session.

    Yields:
        AsyncSession: Active database session.
    """
    async for session in get_async_db():
        yield session


class PaginationParams:
    """Common dependency for paginated API requests."""

    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number"),
        limit: int = Query(default=20, ge=1, le=100, description="Items per page"),
    ) -> None:
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit
