from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy import select, func, delete, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation, Message
from app.conversations.exceptions import ConversationNotFoundException, ConversationForbiddenException


class ConversationRepository:
    """Manages transactional database mappings for Conversation and Message tables, strictly enforcing user boundaries."""

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        conversation_id: str,
        user_id: str,
    ) -> Conversation:
        """Locates a single conversation, verifying that it belongs to the authenticated user.

        Args:
            db (AsyncSession): Database session.
            conversation_id (str): Thread ID.
            user_id (str): Clerk user ID.

        Returns:
            Conversation: The loaded database model.
        """
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await db.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise ConversationNotFoundException(
                message=f"Conversation thread '{conversation_id}' could not be located"
            )

        # Enforce security boundary
        if conversation.user_id != user_id:
            raise ConversationForbiddenException(
                message="You do not have permission to access this conversation thread"
            )

        return conversation

    @staticmethod
    async def list_user_conversations(
        db: AsyncSession,
        user_id: str,
        *,
        skip: int = 0,
        limit: int = 10,
        search_query: Optional[str] = None,
        sort_by: str = "last_activity_at",
        sort_order: str = "desc"
    ) -> Tuple[int, List[Conversation]]:
        """Lists user's conversations with complete query filters, sorting, and pagination.

        Returns:
            Tuple[int, List[Conversation]]: Total matches count and paginated list of models.
        """
        # Build filter query
        where_clause = [Conversation.user_id == user_id]
        if search_query:
            where_clause.append(Conversation.title.ilike(f"%{search_query.strip()}%"))

        combined_filter = and_(*where_clause)

        # 1. Total count query
        count_query = select(func.count(Conversation.id)).where(combined_filter)
        count_res = await db.execute(count_query)
        total_count = count_res.scalar_or_none() or 0

        # 2. Results query with dynamic sorting
        stmt = select(Conversation).where(combined_filter)
        
        # Determine sorting field
        sort_col = getattr(Conversation, sort_by, Conversation.last_activity_at)
        if sort_order.lower() == "asc":
            stmt = stmt.order_by(asc(sort_col))
        else:
            stmt = stmt.order_by(desc(sort_col))

        stmt = stmt.offset(skip).limit(limit)
        results = await db.execute(stmt)
        items = list(results.scalars().all())

        return total_count, items

    @staticmethod
    async def create_conversation(
        db: AsyncSession,
        conversation: Conversation
    ) -> Conversation:
        """Persists a new conversation database record."""
        db.add(conversation)
        await db.flush()
        return conversation

    @staticmethod
    async def add_message_to_conversation(
        db: AsyncSession,
        conversation: Conversation,
        message: Message
    ) -> Message:
        """Appends a nested message to the thread, updating counts and activity markers."""
        db.add(message)
        
        # Touch activity timestamps and counts
        now_time = datetime.now(timezone.utc)
        conversation.message_count += 1
        conversation.last_activity_at = now_time
        conversation.updated_at = now_time

        await db.flush()
        return message

    @staticmethod
    async def delete_conversation(
        db: AsyncSession,
        conversation: Conversation
    ) -> None:
        """Deletes a single conversation model."""
        await db.delete(conversation)
        await db.flush()

    @staticmethod
    async def delete_all_user_conversations(
        db: AsyncSession,
        user_id: str,
    ) -> int:
        """Deletes all conversations for a single Clerk user.

        Returns:
            int: Number of deleted threads.
        """
        stmt = delete(Conversation).where(Conversation.user_id == user_id)
        res = await db.execute(stmt)
        await db.flush()
        return res.rowcount

    @staticmethod
    async def get_user_stats(
        db: AsyncSession,
        user_id: str,
    ) -> Dict[str, Any]:
        """Calculates rich metrics on a user's conversation list."""
        where_clause = Conversation.user_id == user_id

        # Let's write a standard clean CASE query
        case_active = func.sum(func.cast(Conversation.status == "active", func.Integer))
        case_archived = func.sum(func.cast(Conversation.status == "archived", func.Integer))
        
        stmt = select(
            func.count(Conversation.id).label("total"),
            func.sum(Conversation.message_count).label("messages_sum"),
            case_active.label("active"),
            case_archived.label("archived")
        ).where(where_clause)

        result = await db.execute(stmt)
        row = result.fetchone()

        total = row.total if row and row.total else 0
        total_messages = row.messages_sum if row and row.messages_sum else 0
        active = row.active if row and row.active else 0
        archived = row.archived if row and row.archived else 0

        avg = float(total_messages) / total if total > 0 else 0.0

        return {
            "total_conversations": total,
            "active_conversations": active,
            "archived_conversations": archived,
            "total_messages": total_messages,
            "average_messages_per_conversation": round(avg, 2)
        }
