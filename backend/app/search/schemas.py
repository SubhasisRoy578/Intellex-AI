from typing import List, Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Input validation model for dishing out query parameters to active web engines."""

    query: str = Field(..., min_length=1, max_length=1000, description="The textual keywords to locate on the web")
    limit: Optional[int] = Field(None, ge=1, le=50, description="Max result count boundary")


class SearchResult(BaseModel):
    """Standardized representation of a single extracted web result block."""

    title: str = Field(..., description="Title of the web resource")
    url: str = Field(..., description="Absolute URL link reference")
    snippet: str = Field(..., description="Brief snippet containing query context")
    score: float = Field(0.0, description="Relevance rank score")
    source: str = Field(..., description="Origin provider identification name")


class SearchResponse(BaseModel):
    """Unified API response serialization model containing verified web citation details."""

    query: str = Field(..., description="Raw sanitized search query processed")
    results: List[SearchResult] = Field(default_factory=list, description="List of ranked, unique web sources")
    timestamp: float = Field(..., description="Epoch timestamp of search execution completion")


class SearchHealthSchema(BaseModel):
    """Status reporting model for the Internet Search module."""

    status: str = Field(..., description="Operational status of web crawling/search endpoints")
    search_provider: str = Field(..., description="Active resolved crawl engine")
    max_retries_configured: int = Field(..., description="Retries limit active inside backoff loops")
