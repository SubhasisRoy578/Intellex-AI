import time
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.dependencies import get_db_session
from app.core.logging import logger

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Perform a System Health Check",
    description="Validates FastAPI server status, uptime, and PostgreSQL database connectivity.",
)
async def health_check(
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """Verifies that the server and backing databases are fully responsive."""
    start_time = time.time()
    database_status = "unresponsive"
    database_latency = None

    try:
        # Measure latency for simple database ping
        db_start = time.perf_counter()
        await db.execute(text("SELECT 1"))
        database_latency = f"{(time.perf_counter() - db_start) * 1000:.2f}ms"
        database_status = "healthy"
    except Exception as e:
        logger.error(f"Database health probe failed: {e}", exc_info=True)
        database_status = "unhealthy"

    return {
        "status": "healthy" if database_status == "healthy" else "degraded",
        "timestamp": time.time(),
        "services": {
            "api": {
                "status": "healthy",
                "uptime_sec": f"{time.time() - start_time:.4f}"
            },
            "database": {
                "status": database_status,
                "latency": database_latency
            }
        }
    }
