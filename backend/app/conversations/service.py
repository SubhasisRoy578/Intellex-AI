import uuid
import time
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation, Message
from app.conversations.repository import ConversationRepository
from app.conversations.cleanup import ConversationCleanupService
from app.core.logging import logger


class ConversationService:
    """Core Service orchestrating conversation lifecycle transactions and automatic retention prunings."""

    def __init__(self, repository: ConversationRepository = ConversationRepository()) -> None:
        self.repo = repository

    async def create_new_conversation(
        self,
        db: AsyncSession,
        user_id: str,
        title: Optional[str] = None
    ) -> Conversation:
        """Initiates a new conversation session, automatically enforcing the 10-conversation retention limits first."""
        # 1. Trigger automatic cleanup to guarantee room (newest 10 retention policy)
        await ConversationCleanupService.enforce_retention_limit(db, user_id, limit_max=10)

        # 2. Formulate default title if none is provided
        final_title = title.strip() if title and title.strip() else f"Conversation {int(time.time())}"

        now_time = datetime.now(timezone.utc)
        new_thread = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=final_title,
            created_at=now_time,
            updated_at=now_time,
            last_activity_at=now_time,
            message_count=0,
            status="active",
            messages=[]
        )

        # 3. Persist record
        created = await self.repo.create_conversation(db, new_thread)
        logger.info(f"Successfully created a new conversation session: '{created.id}' (Title: {created.title})")
        return created

    async def get_conversation_details(
        self,
        db: AsyncSession,
        conversation_id: str,
        user_id: str
    ) -> Conversation:
        """Retrieves details of a conversation thread, scoping queries strictly to the authenticated owner."""
        return await self.repo.get_by_id(db, conversation_id, user_id)

    async def list_user_threads(
        self,
        db: AsyncSession,
        user_id: str,
        *,
        skip: int = 0,
        limit: int = 10,
        search_query: Optional[str] = None,
        sort_by: str = "last_activity_at",
        sort_order: str = "desc"
    ) -> Tuple[int, List[Conversation]]:
        """Handles lists parsing query filters and pagination."""
        return await self.repo.list_user_conversations(
            db,
            user_id,
            skip=skip,
            limit=limit,
            search_query=search_query,
            sort_by=sort_by,
            sort_order=sort_order
        )

    async def rename_thread(
        self,
        db: AsyncSession,
        conversation_id: str,
        user_id: str,
        title: str,
        status: Optional[str] = None
    ) -> Conversation:
        """Updates and touches properties of an existing conversation thread."""
        thread = await self.repo.get_by_id(db, conversation_id, user_id)

        thread.title = title.strip()
        if status:
            thread.status = status.strip()

        thread.updated_at = datetime.now(timezone.utc)
        await db.flush()

        logger.info(f"Successfully modified properties for conversation '{conversation_id}' (New Title: {thread.title})")
        return thread

    async def remove_thread(
        self,
        db: AsyncSession,
        conversation_id: str,
        user_id: str
    ) -> None:
        """Removes a conversation session by primary ID keys."""
        thread = await self.repo.get_by_id(db, conversation_id, user_id)
        await self.repo.delete_conversation(db, thread)
        logger.info(f"Successfully removed conversation session: '{conversation_id}'")

    async def clear_all_user_threads(
        self,
        db: AsyncSession,
        user_id: str
    ) -> int:
        """Prunes the entire conversations list for a single user."""
        pruned_count = await self.repo.delete_all_user_conversations(db, user_id)
        logger.info(f"Pruned all conversation records for user '{user_id}' (Total Pruned: {pruned_count})")
        return pruned_count

    async def calculate_user_statistics(
        self,
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Runs statistics aggregation for user dashboard listings."""
        return await self.repo.get_user_stats(db, user_id)


# Global default instance
conversation_service = ConversationService()
