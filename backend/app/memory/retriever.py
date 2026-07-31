from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.memory.models import Memory
from app.memory.repository import MemoryRepository
from app.memory.ranking import MemoryRanker


class MemoryRetriever:
    """Pluggable service responsible for fetching, ranking, and formatting long-term memories/preferences for prompt injection."""

    @classmethod
    async def retrieve_context(
        cls,
        db: AsyncSession,
        user_id: str,
        query: str,
        *,
        limit: int = 5,
        category: Optional[str] = None,
        tags: Optional[str] = None
    ) -> List[Memory]:
        """Queries the active memory repository, ranks elements against the input, and returns top matched records.

        Args:
            db (AsyncSession): Database session.
            user_id (str): User identifier.
            query (str): Active prompt query or task text.
            limit (int): Maximum memories to return.
            category (Optional[str]): Categorical filter to restrict memory types.
            tags (Optional[str]): Optional tags filtering string.

        Returns:
            List[Memory]: Ranked list of matching Memory records.
        """
        # 1. Fetch all active memories for the user
        _, active_memories = await MemoryRepository.list_user_memories(
            db=db,
            user_id=user_id,
            category=category,
            is_active=True,
            tags=tags,
            limit=250,  # Grab a larger pool to score in-memory
            sort_by="last_accessed_at",
            sort_order="desc"
        )

        if not active_memories:
            return []

        # 2. Score and rank memories
        required_tags = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
        ranked_pairs = MemoryRanker.rank_memories(
            memories=active_memories,
            query=query,
            limit=limit,
            required_tags=required_tags
        )

        # 3. Touch access of the retrieved memories (updates metrics asynchronously)
        retrieved_memories = []
        for memory, score in ranked_pairs:
            # We only touch if the score indicates some relevance threshold (e.g. > 0.0)
            if score >= 0.1:
                await MemoryRepository.touch_access(db, memory)
                retrieved_memories.append(memory)

        return retrieved_memories

    @classmethod
    def format_context_for_prompt(cls, memories: List[Memory]) -> str:
        """Serializes memories into structured XML context tags for safe, high-fidelity injection into AI system prompts.

        Args:
            memories (List[Memory]): List of matching memory records.

        Returns:
            str: Structured system prompt block.
        """
        if not memories:
            return ""

        context_lines = [
            "==================================================",
            "PERSONALIZATION CONTEXT & LONG-TERM MEMORY",
            "The following facts and preferences about the user are recalled from long-term memory.",
            "Incorporate these preferences seamlessly where relevant to personalize your responses.",
            "=================================================="
        ]

        for i, memory in enumerate(memories, 1):
            category_tag = memory.category.replace(" ", "_").upper()
            context_lines.append(f"<{category_tag} id=\"{memory.id}\" title=\"{memory.title}\">")
            context_lines.append(memory.content.strip())
            context_lines.append(f"</{category_tag}>")

        context_lines.append("==================================================")
        return "\n".join(context_lines)
