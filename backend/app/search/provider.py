import os
import httpx
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.config.config import settings
from app.core.logging import logger
from app.search.exceptions import SearchProviderException, SearchTimeoutException


class BaseSearchProvider(ABC):
    """Abstract interface defining boundary contracts for interchangeable internet crawling engines."""

    @abstractmethod
    async def execute_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Asynchronously dispatches a textual query to the target web provider.

        Args:
            query (str): Keyword query prompt.
            limit (int): Maximum number of results to fetch.

        Returns:
            List[Dict[str, Any]]: List of dictionary structures containing fields:
                - "title" (str)
                - "url" (str)
                - "snippet" (str)
                - "score" (float)
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the registered code identifier of this search crawler (e.g. 'tavily', 'mock')."""
        pass


class MockSearchProvider(BaseSearchProvider):
    """Linguistic matching mock crawler providing rich realistic web citations."""

    async def execute_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        logger.info(f"MockSearch executing crawled lookup for: '{query}'")
        query_lower = query.lower()

        # Predefined rich mock results based on domain keywords
        results = [
            {
                "title": "Intellex AI Assistant - Premium Architecture Overview",
                "url": "https://intellex.ai/blog/premium-architecture",
                "snippet": "Exploring the decoupled architecture, structured logging, and unified JWT validation boundaries of Intellex AI backend.",
                "score": 0.98,
            },
            {
                "title": "FastAPI Best Practices for Cloud-Native Backends",
                "url": "https://fastapi.tiangolo.com/best-practices",
                "snippet": "Production guidelines for building robust modular routes, exception handlers, and secure file uploads in Python 3.12.",
                "score": 0.92,
            },
            {
                "title": "Clerk JWT Integration with Python Web Frameworks",
                "url": "https://clerk.com/docs/backend/jwt-verification",
                "snippet": "Configuring local RS256 JWKS public keys decryption to verify Clerk session tokens asynchronously with low latency.",
                "score": 0.89,
            },
            {
                "title": "PyMuPDF & python-docx Memory Management Guidelines",
                "url": "https://pymupdf.readthedocs.io/en/latest/memory",
                "snippet": "Linguistic count analysis pipelines, unicode normalizations, and memory buffer stream disposals for PDF and Word processing.",
                "score": 0.85,
            },
            {
                "title": "Pillow Image Preprocessing and Contrast Boosting for OCR",
                "url": "https://pillow.readthedocs.io/en/stable/enhancements",
                "snippet": "Improving Tesseract text recognition confidence using grayscale, contrast enhancers, and exif_transpose rotation handling.",
                "score": 0.82,
            }
        ]

        # Filter results based on keywords if matches found, otherwise return full list trimmed
        matches = [r for r in results if any(w in r["title"].lower() or w in r["snippet"].lower() for w in query_lower.split())]
        final_list = matches if matches else results

        return final_list[:limit]

    def get_provider_name(self) -> str:
        return "mock"


class TavilySearchProvider(BaseSearchProvider):
    """Asynchronous production-ready Tavily Search API Provider using raw httpx queries."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.api_url = "https://api.tavily.com/search"

    async def execute_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        headers = {"Content-Type": "application/json"}
        data = {
            "api_key": self.api_key,
            "query": query,
            "max_results": limit,
            "include_answer": False,
            "include_raw_content": False,
        }

        async with httpx.AsyncClient(timeout=settings.SEARCH_TIMEOUT_SECONDS) as client:
            try:
                response = await client.post(self.api_url, headers=headers, json=data)

                if response.status_code != 200:
                    logger.error(f"Tavily error reply: {response.text}")
                    raise SearchProviderException(
                        message="Tavily provider failed to retrieve search results",
                        details={"status_code": response.status_code, "error": response.text}
                    )

                result_json = response.json()
                raw_results = result_json.get("results", [])

                # Standardize Tavily output fields to match BaseSearchProvider contract
                standardized = []
                for res in raw_results:
                    standardized.append({
                        "title": res.get("title", "Untitled"),
                        "url": res.get("url", ""),
                        "snippet": res.get("content", ""),
                        "score": res.get("score", 0.0),
                    })
                return standardized

            except httpx.TimeoutException as e:
                logger.warning(f"Tavily search request timed out: {e}")
                raise SearchTimeoutException(message="Tavily search request timed out")
            except Exception as e:
                if isinstance(e, (SearchProviderException, SearchTimeoutException)):
                    raise e
                logger.error(f"Error querying Tavily search: {e}", exc_info=True)
                raise SearchProviderException(message="Failed to communicate with Tavily Search API")

    def get_provider_name(self) -> str:
        return "tavily"
