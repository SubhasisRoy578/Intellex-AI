from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.config import settings
from app.core.logging import logger
from app.api.v1 import api_router
from app.exceptions.exceptions import register_exception_handlers
from app.middleware.middleware import CorrelationAndPerformanceMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for managing FastAPI startup and shutdown lifecycle events."""
    # STARTUP ACTIONS
    logger.info(
        f"Starting up {settings.APP_NAME} in environment: {settings.APP_ENV}...",
        extra={"extra": {"environment": settings.APP_ENV, "debug_mode": settings.DEBUG}}
    )
    yield
    # SHUTDOWN ACTIONS
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-ready production-grade Backend API Foundation for Intellex AI Assistant.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# 1. Register Global CORS Middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 2. Register Request-ID Correlation & Performance Monitoring Middleware
app.add_middleware(CorrelationAndPerformanceMiddleware)

# 3. Register Centralized Exceptions and Validation Formatters
register_exception_handlers(app)

# 4. Mount Versioned Router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root endpoint
@app.get("/", tags=["Root"])
async def root_index() -> JSONResponse:
    """Root entrypoint returning general API information."""
    return JSONResponse(
        content={
            "app_name": settings.APP_NAME,
            "version": "1.0.0",
            "documentation": "/docs",
            "status": "online",
        }
    )
