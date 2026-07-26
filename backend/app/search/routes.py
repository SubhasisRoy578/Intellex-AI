from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser
from app.search.schemas import SearchRequest, SearchResponse, SearchHealthSchema, SearchResult
from app.search.service import search_service, SearchService
from app.search.factory import SearchProviderFactory
from app.config.config import settings

router = APIRouter(prefix="/search", tags=["Latest Internet Search Integration"])


@router.post(
    "",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search the Internet",
    description="Asynchronously crawls and queries configured search providers for up-to-date web articles, sanitizing and deduplicating outputs.",
)
async def query_internet(
    request: SearchRequest,
    current_user: ClerkUser = Depends(get_current_user),
) -> SearchResponse:
    """Dispatches search prompt queries to crawl standard providers securely."""
    result = await search_service.execute_web_search(
        query=request.query,
        limit=request.limit
    )

    standard_results = []
    for item in result["results"]:
        standard_results.append(SearchResult(
            title=item["title"],
            url=item["url"],
            snippet=item["snippet"],
            score=item["score"],
            source=item["source"]
        ))
    
    return SearchResponse(
        query=result["query"],
        results=standard_results,
        timestamp=result["timestamp"],
    )


@router.get(
    "/health",
    response_model=SearchHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Internet Search Module Health",
    description="Validates and reports configuration properties for web crawlers.",
)
async def check_search_health() -> SearchHealthSchema:
    """Reports configuration attributes for the search indexing module."""
    provider = SearchProviderFactory.get_provider()
    return SearchHealthSchema(
        status="healthy" if provider.get_provider_name() else "degraded",
        search_provider=provider.get_provider_name(),
        max_retries_configured=settings.SEARCH_MAX_RETRIES,
    )
