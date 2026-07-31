import time
import asyncio
from typing import List, Dict, Any, Optional
from app.config.config import settings
from app.core.logging import logger
from app.search.provider import BaseSearchProvider
from app.search.factory import SearchProviderFactory
from app.search.citations import CitationBuilder
from app.search.exceptions import SearchProviderException, SearchTimeoutException


class SearchService:
    """Core orchestrator service handling query processing, backoff retries, and result normalization."""

    def __init__(self, provider: Optional[BaseSearchProvider] = None) -> None:
        self.provider = provider or SearchProviderFactory.get_provider()

    async def execute_web_search(
        self,
        query: str,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Dispatches keywords to the active provider with built-in retry and citation compiling.

        Args:
            query (str): Keyword prompt query.
            limit (Optional[int]): Max quantity threshold.

        Returns:
            Dict[str, Any]: Ranked and cleaned results map.
        """
        # Resolve limit
        max_results = limit or settings.SEARCH_DEFAULT_LIMIT
        max_retries = settings.SEARCH_MAX_RETRIES
        delay = 1.0
        last_exception = None

        logger.info(
            f"Dispatching query to Search Provider '{self.provider.get_provider_name()}'...",
            extra={
                "extra": {
                    "query": query,
                    "max_results": max_results,
                    "provider": self.provider.get_provider_name()
                }
            }
        )

        raw_results = []
        for attempt in range(1, max_retries + 1):
            try:
                raw_results = await self.provider.execute_search(query, max_results)
                break
            except (SearchProviderException, SearchTimeoutException) as exc:
                last_exception = exc
                logger.warning(
                    f"Search attempt {attempt}/{max_retries} failed: {exc.message}",
                    extra={"extra": {"attempt": attempt, "error": str(exc)}}
                )
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                    delay *= 2  # Exponential backoff
            except Exception as exc:
                last_exception = exc
                logger.error(
                    f"Unexpected error in execute_web_search attempt {attempt}/{max_retries}: {exc}",
                    exc_info=True
                )
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                    delay *= 2

        if last_exception and not raw_results:
            raise last_exception

        # 1. Deduplicate by canonical URLs
        unique_results = CitationBuilder.deduplicate_results(raw_results)

        # 2. Rank and sort by relevance score
        sorted_results = CitationBuilder.rank_and_sort(unique_results)

        # 3. Format result block structures
        standard_results = []
        for item in sorted_results:
            standard_results.append({
                "title": item.get("title", "Untitled"),
                "url": item.get("url", ""),
                "snippet": item.get("snippet", ""),
                "score": item.get("score", 0.0),
                "source": self.provider.get_provider_name(),
            })

        logger.info(
            f"Search succeeded. Extracted {len(standard_results)} unique citations.",
            extra={"extra": {"results_count": len(standard_results)}}
        )

        return {
            "query": query,
            "results": standard_results,
            "timestamp": time.time()
        }


# Global default instance
search_service = SearchService()
