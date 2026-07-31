import httpx
from typing import AsyncGenerator
from app.config.config import settings

# Reuse a single asynchronous HTTPX client pool to optimize connection speeds and save socket descriptors
_async_client: httpx.AsyncClient = httpx.AsyncClient(
    timeout=settings.SEARCH_TIMEOUT_SECONDS,
    limits=httpx.Limits(max_keepalive_connections=5, max_connections=20),
)


async def get_search_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Dependency injection generator providing a high-performance shared HTTP client pool."""
    yield _async_client
