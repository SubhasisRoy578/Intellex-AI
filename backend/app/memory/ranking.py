import re
from typing import List, Set, Dict, Any, Tuple
from app.memory.models import Memory


class MemoryRanker:
    """Implements keyword relevance, tag alignment, and importance scoring to rank memory records for system context injection."""

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        """Normalizes and tokenizes a string of text into a lowercase alphabetic word set."""
        if not text:
            return set()
        # Strip punctuation, convert to lowercase and split
        normalized = re.sub(r"[^\w\s]", "", text.lower())
        return {word for word in normalized.split() if len(word) > 2}

    @classmethod
    def calculate_relevance_score(
        cls,
        memory: Memory,
        query_tokens: Set[str],
        query_tags: Set[str] = None
    ) -> float:
        """Calculates a numerical score indicating how relevant a memory item is to a tokenized user query.

        Relevance is calculated using a compound weight of:
        1. Keyword match density (intersection over union between query tokens and memory title/content).
        2. Exact tag alignments (boosts score if memory tags match queried tags).
        3. Static importance score of the memory (guarantees prioritized injection of critical user preferences).

        Args:
            memory (Memory): The memory record database model.
            query_tokens (Set[str]): Lowercase tokenized keywords from user input query.
            query_tags (Set[str]): Specific tags being searched or matching the request.

        Returns:
            float: Combined scoring from 0.0 to 10.0+.
        """
        if not query_tokens:
            # Fallback to pure importance if no query tokens are supplied
            return memory.importance_score * 2.0

        # Tokenize memory fields
        title_tokens = cls._tokenize(memory.title)
        content_tokens = cls._tokenize(memory.content)
        memory_tokens = title_tokens.union(content_tokens)

        # 1. Calculate Keyword Intersection Match
        intersection = query_tokens.intersection(memory_tokens)
        if not intersection:
            keyword_score = 0.0
        else:
            # Title matches are weighted heavier than content matches
            title_intersection = query_tokens.intersection(title_tokens)
            keyword_score = (len(intersection) / len(query_tokens)) * 3.0
            if title_intersection:
                keyword_score += len(title_intersection) * 1.5

        # 2. Tag Alignment Boost
        tag_score = 0.0
        if query_tags and memory.tags:
            memory_tag_set = {t.strip().lower() for t in memory.tags.split(",") if t.strip()}
            matching_tags = query_tags.intersection(memory_tag_set)
            if matching_tags:
                tag_score = len(matching_tags) * 2.0

        # 3. Base Importance Score (0.0 to 1.0)
        # Scale importance score to have a meaningful boost
        importance_boost = memory.importance_score * 2.5

        # Compound score formulation
        total_score = keyword_score + tag_score + importance_boost
        return round(total_score, 4)

    @classmethod
    def rank_memories(
        cls,
        memories: List[Memory],
        query: str,
        limit: int = 5,
        required_tags: List[str] = None
    ) -> List[Tuple[Memory, float]]:
        """Ranks a list of memories based on context relevance and returns top-K records.

        Args:
            memories (List[Memory]): List of memory DB models.
            query (str): User input string to compute matching scores against.
            limit (int): Max number of memories to return.
            required_tags (List[str]): List of tags expected in query context.

        Returns:
            List[Tuple[Memory, float]]: Sorted list of (Memory, score) tuples in descending order.
        """
        if not memories:
            return []

        query_tokens = cls._tokenize(query)
        query_tag_set = {t.strip().lower() for t in required_tags} if required_tags else set()

        scored_memories: List[Tuple[Memory, float]] = []
        for memory in memories:
            score = cls.calculate_relevance_score(memory, query_tokens, query_tag_set)
            scored_memories.append((memory, score))

        # Sort descending by score
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return scored_memories[:limit]
