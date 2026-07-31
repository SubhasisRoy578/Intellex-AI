from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy import select, func, delete, and_, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.memory.models import Memory
from app.memory.exceptions import MemoryNotFoundException, MemoryForbiddenException


class MemoryRepository:
    """Manages transactional database operations for the Memory model, enforcing user boundary boundaries."""

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        memory_id: str,
        user_id: str,
    ) -> Memory:
        """Locates a single memory record, validating ownership.

        Args:
            db (AsyncSession): Database session.
            memory_id (str): UUID string.
            user_id (str): Clerk user ID.

        Returns:
            Memory: The retrieved DB model.

        Raises:
            MemoryNotFoundException: If the record doesn't exist.
            MemoryForbiddenException: If ownership belongs to a different user.
        """
        query = select(Memory).where(Memory.id == memory_id)
        result = await db.execute(query)
        record = result.scalar_one_or_none()

        if not record:
            raise MemoryNotFoundException(
                message=f"Memory record with ID '{memory_id}' could not be located."
            )

        # Enforce security boundaries
        if record.user_id != user_id:
            raise MemoryForbiddenException(
                message="Access to this memory record is forbidden."
            )

        return record

    @staticmethod
    async def list_user_memories(
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
        """Lists memories matching user ID, utilizing dynamic sorting, pagination, and various filters.

        Args:
            db (AsyncSession): Database session.
            user_id (str): Clerk user ID.
            category (Optional[str]): Categorical filter.
            is_active (Optional[bool]): Active status filter.
            search_query (Optional[str]): Text search against title or content.
            tags (Optional[str]): Specific tags substring filter.
            skip (int): Pagination offset.
            limit (int): Pagination limit.
            sort_by (str): DB column name to sort by.
            sort_order (str): sorting order 'asc' or 'desc'.

        Returns:
            Tuple[int, List[Memory]]: Total count of matching records and list of Memory models.
        """
        where_clause = [Memory.user_id == user_id]

        if category:
            where_clause.append(Memory.category == category.strip())

        if is_active is not None:
            where_clause.append(Memory.is_active == is_active)

        if search_query:
            query_str = f"%{search_query.strip()}%"
            where_clause.append(
                or_(
                    Memory.title.ilike(query_str),
                    Memory.content.ilike(query_str)
                )
            )

        if tags:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            tag_filters = []
            for t in tag_list:
                tag_filters.append(Memory.tags.ilike(f"%{t}%"))
            if tag_filters:
                where_clause.append(or_(*tag_filters))

        combined_filter = and_(*where_clause)

        # 1. Query matching count
        count_query = select(func.count(Memory.id)).where(combined_filter)
        count_res = await db.execute(count_query)
        total_count = count_res.scalar_or_none() or 0

        # 2. Query actual records
        stmt = select(Memory).where(combined_filter)

        # Fallback sorting column
        sort_col = getattr(Memory, sort_by, Memory.last_accessed_at)
        if sort_order.lower() == "asc":
            stmt = stmt.order_by(asc(sort_col))
        else:
            stmt = stmt.order_by(desc(sort_col))

        stmt = stmt.offset(skip).limit(limit)
        results = await db.execute(stmt)
        items = list(results.scalars().all())

        return total_count, items

    @staticmethod
    async def create_memory(
        db: AsyncSession,
        memory: Memory
    ) -> Memory:
        """Persists a new memory database record."""
        db.add(memory)
        await db.flush()
        return memory

    @staticmethod
    async def touch_access(
        db: AsyncSession,
        memory: Memory
    ) -> Memory:
        """Updates last_accessed_at time and increments access_count."""
        memory.last_accessed_at = datetime.now(timezone.utc)
        memory.access_count += 1
        await db.flush()
        return memory

    @staticmethod
    async def delete_memory(
        db: AsyncSession,
        memory: Memory
    ) -> None:
        """Deletes a memory record."""
        await db.delete(memory)
        await db.flush()

    @staticmethod
    async def delete_all_user_memories(
        db: AsyncSession,
        user_id: str,
    ) -> int:
        """Deletes all memory records associated with a specific user."""
        stmt = delete(Memory).where(Memory.user_id == user_id)
        res = await db.execute(stmt)
        await db.flush()
        return res.rowcount

    @staticmethod
    async def get_stats(
        db: AsyncSession,
        user_id: str,
    ) -> Dict[str, Any]:
        """Calculates memory usage statistics and distribution categorized by users.

        Returns:
            Dict[str, Any]: total, active counts and category counts.
        """
        # Count total
        total_stmt = select(func.count(Memory.id)).where(Memory.user_id == user_id)
        total_res = await db.execute(total_stmt)
        total_count = total_res.scalar_or_none() or 0

        # Count active
        active_stmt = select(func.count(Memory.id)).where(
            and_(Memory.user_id == user_id, Memory.is_active == True)
        )
        active_res = await db.execute(active_stmt)
        active_count = active_res.scalar_or_none() or 0

        # Categories list with count
        cat_stmt = (
            select(Memory.category, func.count(Memory.id))
            .where(Memory.user_id == user_id)
            .group_by(Memory.category)
        )
        cat_res = await db.execute(cat_stmt)
        categories_stats = [
            {"category": cat, "count": count} for cat, count in cat_res.all()
        ]

        return {
            "total_memories": total_count,
            "active_memories": active_count,
            "categories": categories_stats
        }
