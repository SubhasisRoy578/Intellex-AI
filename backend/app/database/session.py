from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.database.database import engine

# Async session factory
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency generator to retrieve an asynchronous database session.

    Yields:
        AsyncSession: Thread-safe, transaction-isolated async session.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
