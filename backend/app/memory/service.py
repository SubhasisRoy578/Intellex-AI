from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.memory.models import Memory
from app.memory.schemas import MemoryCreate, MemoryUpdate, MemoryStats, MemoryResponse
from app.memory.manager import MemoryManager


class MemoryService:
    """Service layer that decouples REST API controllers from underlying repository and management transactions."""

    @staticmethod
    async def create_memory(
        db: AsyncSession,
        user_id: str,
        payload: MemoryCreate
    ) -> Memory:
        """Triggers secure creation of user-specific memory or preference record."""
        return await MemoryManager.create_user_memory(db, user_id=user_id, schema=payload)

    @staticmethod
    async def get_memory(
        db: AsyncSession,
        memory_id: str,
        user_id: str
    ) -> Memory:
        """Finds a single user-owned memory record with secure authorization validation."""
        return await MemoryManager.get_user_memory(db, memory_id=memory_id, user_id=user_id)

    @staticmethod
    async def list_memories(
        db: AsyncSession,
        user_id: str,
        *,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        search_query: Optional[str] = None,
        tags: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
        sort_by: str = "last_accessed_at",
        sort_order: str = "desc"
    ) -> Tuple[int, List[Memory]]:
        """Queries and returns filtered user memories."""
        return await MemoryManager.list_memories(
            db=db,
            user_id=user_id,
            category=category,
            is_active=is_active,
            search_query=search_query,
            tags=tags,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )

    @staticmethod
    async def update_memory(
        db: AsyncSession,
        memory_id: str,
        user_id: str,
        payload: MemoryUpdate
    ) -> Memory:
        """Modifies and saves active attributes of a selected memory record."""
        return await MemoryManager.update_user_memory(
            db=db,
            memory_id=memory_id,
            user_id=user_id,
            schema=payload
        )

    @staticmethod
    async def delete_memory(
        db: AsyncSession,
        memory_id: str,
        user_id: str
    ) -> None:
        """Removes a user's memory record permanently."""
        await MemoryManager.delete_user_memory(db, memory_id=memory_id, user_id=user_id)

    @staticmethod
    async def clear_memories(
        db: AsyncSession,
        user_id: str
    ) -> int:
        """Saves a soft or hard purge request to clear all user-associated memory metadata."""
        return await MemoryManager.purge_user_memories(db, user_id=user_id)

    @staticmethod
    async def retrieve_metrics(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Provides metadata statistics of memory records grouped by active status and category."""
        return await MemoryManager.get_user_stats(db, user_id=user_id)

    @staticmethod
    async def trigger_extraction(
        db: AsyncSession,
        user_id: str,
        dialogue: str
    ) -> List[Memory]:
        """Interprets dialog string to extract preference insights."""
        return await MemoryManager.auto_extract_facts_from_text(db=db, user_id=user_id, text_content=dialogue)
