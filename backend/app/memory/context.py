from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.memory.models import Memory
from app.memory.retriever import MemoryRetriever


class MemoryContextComposer:
    """Orchestrates comprehensive long-term context creation by querying, ranking, and blending user memories and preferences."""

    @classmethod
    async def get_system_prompt_addition(
        cls,
        db: AsyncSession,
        user_id: str,
        user_query: str,
        *,
        limit: int = 5,
        category: Optional[str] = None,
        tags: Optional[str] = None
    ) -> str:
        """Retrieves and formats user-specific long-term preferences, project information, and facts as a system prompt segment.

        Args:
            db (AsyncSession): Database session.
            user_id (str): Clerk user ID.
            user_query (str): Active message or text prompt.
            limit (int): Maximum memories to extract.
            category (Optional[str]): Limit search to a specific memory type if needed.
            tags (Optional[str]): Tag filter parameters.

        Returns:
            str: System prompt segment block (empty if no memories are found or registered).
        """
        # Fetch matching and ranked memories
        memories = await MemoryRetriever.retrieve_context(
            db=db,
            user_id=user_id,
            query=user_query,
            limit=limit,
            category=category,
            tags=tags
        )

        if not memories:
            return ""

        # Format retrieved items into system-injectable structures
        return MemoryRetriever.format_context_for_prompt(memories)

    @classmethod
    async def get_orchestrator_payload(
        cls,
        db: AsyncSession,
        user_id: str,
        user_query: str,
        *,
        limit: int = 5
    ) -> Dict[str, Any]:
        """Assembles a structured memory payload for deep diagnostic or API orchestration logs.

        Args:
            db (AsyncSession): Database session.
            user_id (str): Clerk user ID.
            user_query (str): Active instruction query.
            limit (int): Maximum records.

        Returns:
            Dict[str, Any]: Descriptive dictionary representation containing raw elements and the formatted block.
        """
        memories = await MemoryRetriever.retrieve_context(
            db=db,
            user_id=user_id,
            query=user_query,
            limit=limit
        )

        formatted_block = MemoryRetriever.format_context_for_prompt(memories)

        return {
            "retrieved_count": len(memories),
            "memories": [
                {
                    "id": m.id,
                    "category": m.category,
                    "title": m.title,
                    "importance_score": m.importance_score,
                    "tags": m.tags,
                    "access_count": m.access_count
                }
                for m in memories
            ],
            "system_prompt_block": formatted_block
        }
