import re
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.memory.models import Memory
from app.memory.schemas import MemoryCreate, MemoryUpdate
from app.memory.repository import MemoryRepository
from app.memory.ranking import MemoryRanker
from app.core.logging import logger


class MemoryManager:
    """Consolidated business logic and orchestration management for personalization and long-term memory operations."""

    @classmethod
    async def create_user_memory(
        cls,
        db: AsyncSession,
        user_id: str,
        schema: MemoryCreate
    ) -> Memory:
        """Saves a new user memory preference or profile fact.

        Args:
            db (AsyncSession): Database session.
            user_id (str): Associated Clerk User ID.
            schema (MemoryCreate): Input parameters.

        Returns:
            Memory: The newly created database record.
        """
        now = datetime.now(timezone.utc)
        memory = Memory(
            id=str(uuid.uuid4()),
            user_id=user_id,
            category=schema.category.strip(),
            title=schema.title.strip(),
            content=schema.content.strip(),
            importance_score=schema.importance_score,
            source=schema.source.strip(),
            tags=schema.tags.strip(),
            is_active=schema.is_active,
            created_at=now,
            updated_at=now,
            last_accessed_at=now,
            access_count=0
        )
        logger.info(f"Creating long-term memory for user '{user_id}': category='{memory.category}', title='{memory.title}'")
        return await MemoryRepository.create_memory(db, memory)

    @classmethod
    async def get_user_memory(
        cls,
        db: AsyncSession,
        memory_id: str,
        user_id: str
    ) -> Memory:
        """Retrieves a specific user memory with secure user ownership checks.

        Args:
            db (AsyncSession): Database session.
            memory_id (str): Unique UUID string.
            user_id (str): Clerk user ID.

        Returns:
            Memory: Loaded database model.
        """
        return await MemoryRepository.get_by_id(db, memory_id=memory_id, user_id=user_id)

    @classmethod
    async def list_memories(
        cls,
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
        """Lists user memories with full pagination, matching patterns, and sorting configurations."""
        return await MemoryRepository.list_user_memories(
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

    @classmethod
    async def update_user_memory(
        cls,
        db: AsyncSession,
        memory_id: str,
        user_id: str,
        schema: MemoryUpdate
    ) -> Memory:
        """Updates fields of an existing memory record.

        Args:
            db (AsyncSession): Database session.
            memory_id (str): UUID string.
            user_id (str): Clerk user ID.
            schema (MemoryUpdate): Fields to update.

        Returns:
            Memory: Updated database model.
        """
        memory = await MemoryRepository.get_by_id(db, memory_id=memory_id, user_id=user_id)

        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if isinstance(value, str):
                    setattr(memory, key, value.strip())
                else:
                    setattr(memory, key, value)

        memory.updated_at = datetime.now(timezone.utc)
        await db.flush()

        logger.info(f"Updated memory record '{memory_id}' for user '{user_id}'")
        return memory

    @classmethod
    async def delete_user_memory(
        cls,
        db: AsyncSession,
        memory_id: str,
        user_id: str
    ) -> None:
        """Deletes a single memory record securely."""
        memory = await MemoryRepository.get_by_id(db, memory_id=memory_id, user_id=user_id)
        await MemoryRepository.delete_memory(db, memory)
        logger.info(f"Deleted memory record '{memory_id}' for user '{user_id}'")

    @classmethod
    async def purge_user_memories(
        cls,
        db: AsyncSession,
        user_id: str
    ) -> int:
        """Purges/deletes all memory records associated with a specific user."""
        logger.warning(f"Purging ALL long-term memory records for user '{user_id}'")
        return await MemoryRepository.delete_all_user_memories(db, user_id=user_id)

    @classmethod
    async def get_user_stats(
        cls,
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Calculates volume metrics and category distribution for a user's memories."""
        return await MemoryRepository.get_stats(db, user_id=user_id)

    @classmethod
    async def auto_extract_facts_from_text(
        cls,
        db: AsyncSession,
        user_id: str,
        text_content: str
    ) -> List[Memory]:
        """Scans a raw message exchanges/conversation texts to extract facts or preferences automatically.

        In a production environment, this would call a LLM or JSON extractor to identify patterns like:
        'I prefer Python over Node.js' -> preference: 'Python'
        In this lightweight implementation, we perform high-confidence regex matching rules to detect explicit preferences,
        simulating an automated background AI extraction pipeline with zero heavy model calls.

        Args:
            db (AsyncSession): Database session.
            user_id (str): Clerk user ID.
            text_content (str): Incoming/outgoing user prompts.

        Returns:
            List[Memory]: List of newly generated active memories extracted from the prompt.
        """
        extracted_memories: List[Memory] = []
        if not text_content:
            return extracted_memories

        # Simple semantic-regex pattern extraction for common long-term facts
        patterns = [
            (r"(?:my preferred|i prefer|i like to use|i always use)\s+([\w\s\-]{2,30})\s+(?:for|instead|when|to)", "preferences", "Preferred Technology"),
            (r"(?:my email is|contact me at)\s+([\w\.-]+@[\w\.-]+\.\w+)", "long_term_facts", "User Contact Info"),
            (r"(?:i am working on|my active project is|currently developing)\s+([\w\s\-]{2,40})", "projects", "Active Project"),
            (r"(?:my coding framework of choice is|i love using)\s+([\w\s\-]{2,30})", "preferences", "Coding Preference")
        ]

        for regex, category, title_prefix in patterns:
            match = re.search(regex, text_content, re.IGNORECASE)
            if match:
                extracted_value = match.group(1).strip()
                # Skip false positives or excessively long junk extracts
                if len(extracted_value) < 2 or len(extracted_value) > 100:
                    continue

                # Check if a matching fact already exists to prevent duplicate spamming
                _, existing = await MemoryRepository.list_user_memories(
                    db=db,
                    user_id=user_id,
                    category=category,
                    search_query=extracted_value,
                    limit=1
                )

                if not existing:
                    new_mem = MemoryCreate(
                        category=category,
                        title=f"{title_prefix}: {extracted_value[:30]}",
                        content=f"Extracted from conversation: User mentioned preference/fact matching '{extracted_value}'.",
                        importance_score=0.6,
                        source="ai_extracted",
                        tags=f"extracted,{category}",
                        is_active=True
                    )
                    saved = await cls.create_user_memory(db, user_id=user_id, schema=new_mem)
                    extracted_memories.append(saved)

        return extracted_memories
