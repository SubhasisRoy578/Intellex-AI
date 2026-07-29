import time
import asyncio
from typing import Dict, Tuple, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.config.config import settings
from app.core.logging import logger


class InMemoryRateLimiterMiddleware(BaseHTTPMiddleware):
    """Thread-safe, token-bucket-based rate limiter middleware restricting requests per client IP or User ID."""

    def __init__(self, app: Any) -> None:
        super().__init__(app)
        # Maps client_key -> (tokens_count, last_update_timestamp)
        self.buckets: Dict[str, Tuple[float, float]] = {}
        self.lock = asyncio.Lock()
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        self.capacity = settings.RATE_LIMIT_PER_MINUTE
        # Fill rate: tokens per second
        self.fill_rate = self.rate_limit / 60.0

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> JSONResponse: # type: ignore
        # Exclude liveness/readiness/docs checks from rate limits to prevent probe failures
        path = request.url.path
        if path.endswith("/liveness") or path.endswith("/readiness") or "docs" in path or "openapi" in path:
            return await call_next(request)

        # Resolve client identifier key (fallback to IP if auth has not processed yet)
        client_key = request.client.host if request.client else "unknown_ip"
        
        # Enforce rate limiter checks
        async with self.lock:
            now = time.time()
            tokens, last_update = self.buckets.get(client_key, (self.capacity, now))

            # Replenish tokens based on elapsed duration
            elapsed = now - last_update
            new_tokens = min(self.capacity, tokens + (elapsed * self.fill_rate))

            if new_tokens >= 1.0:
                self.buckets[client_key] = (new_tokens - 1.0, now)
            else:
                self.buckets[client_key] = (new_tokens, now)
                retry_after = (1.0 - new_tokens) / self.fill_rate
                logger.warning(
                    f"Rate limit exceeded for client {client_key}. Rejection active.",
                    extra={"extra": {"client": client_key, "retry_after_sec": f"{retry_after:.2f}"}}
                )
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "success": False,
                        "error": {
                            "code": status.HTTP_429_TOO_MANY_REQUESTS,
                            "message": "Too many requests. Please slow down.",
                            "details": {"retry_after_sec": round(retry_after, 2)}
                        }
                    },
                    headers={"Retry-After": f"{retry_after:.2f}"}
                )

        return await call_next(request)
