from sqlalchemy import select, func, asc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation
from app.core.logging import logger


class ConversationCleanupService:
    """Automates user conversation retention bounds, pruning oldest records to maintain newest 10 limit."""

    @staticmethod
    async def enforce_retention_limit(
        db: AsyncSession,
        user_id: str,
        limit_max: int = 10,
    ) -> int:
        """Enforces conversation count limitations, deleting oldest entries if count >= limit_max.

        Args:
            db (AsyncSession): Database session.
            user_id (str): Clerk user ID.
            limit_max (int): Allowed ceiling before triggering pruning.

        Returns:
            int: Total records pruned.
        """
        # 1. Fetch current user conversations count
        stmt = select(func.count(Conversation.id)).where(Conversation.user_id == user_id)
        count_res = await db.execute(stmt)
        current_count = count_res.scalar_or_none() or 0

        if current_count < limit_max:
            # We are within safe limits
            return 0

        # Calculate excess count to prune
        excess_count = (current_count - limit_max) + 1
        logger.info(
            f"User '{user_id}' has {current_count} conversations. "
            f"Enforcing retention limit: Pruning {excess_count} oldest threads..."
        )

        # 2. Select oldest conversations (sorted by last_activity_at asc)
        oldest_stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(asc(Conversation.last_activity_at))
            .limit(excess_count)
        )
        oldest_res = await db.execute(oldest_stmt)
        oldest_threads = oldest_res.scalars().all()

        # 3. Perform pruning deletions
        pruned = 0
        for thread in oldest_threads:
            await db.delete(thread)
            pruned += 1
            logger.info(f"Retention Cleanup: Automatically pruned oldest conversation thread '{thread.id}' ({thread.title})")

        # Flush mutations to session transaction
        await db.flush()
        return pruned
