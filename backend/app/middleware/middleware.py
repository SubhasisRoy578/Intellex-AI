import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.logging import logger


class CorrelationAndPerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware for injecting Request ID correlation headers, tracking

    execution performance, and handling global requests/responses logging.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Get request ID from incoming headers or generate a new UUID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Attach request_id to state so it's accessible down the stack
        request.state.request_id = request_id

        start_time = time.perf_counter()
        
        # Log request receipt
        logger.info(
            f"Incoming request {request.method} {request.url.path}",
            extra={
                "extra": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": str(request.query_params),
                    "client_host": request.client.host if request.client else None,
                }
            },
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            # Handle unexpected exceptions elegantly and measure latency
            duration = time.perf_counter() - start_time
            logger.error(
                f"Request failed: {exc}",
                exc_info=True,
                extra={
                    "extra": {
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "duration_sec": f"{duration:.4f}",
                    }
                },
            )
            raise exc

        duration = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration:.4f}"

        # Log request success and completion metrics
        logger.info(
            f"Completed request {request.method} {request.url.path} with status {response.status_code} in {duration:.4f}s",
            extra={
                "extra": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_sec": f"{duration:.4f}",
                }
            },
        )

        return response
