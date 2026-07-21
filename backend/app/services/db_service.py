from typing import Generic, Type, TypeVar, Optional, List, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class DBBaseService(Generic[ModelType]):
    """Generic base database service class providing CRUD logic."""

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Fetch a record by primary key."""
        result = await db.get(self.model, id)
        return result

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Fetch multiple records with pagination."""
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: ModelType) -> ModelType:
        """Create a new database record."""
        db.add(obj_in)
        await db.flush()
        return obj_in

    async def remove(self, db: AsyncSession, *, id: Any) -> Optional[ModelType]:
        """Remove a database record by primary key."""
        obj = await db.get(self.model, id)
        if obj:
            await db.delete(obj)
            await db.flush()
        return obj
