from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.dependencies import get_db_session
from app.monitoring.diagnostics import SystemDiagnostics

router = APIRouter(prefix="/monitoring", tags=["System Performance & Monitoring"])


@router.get(
    "/liveness",
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Indicates whether the container process is running. Always returns 200.",
)
async def check_liveness() -> dict:
    """Standard liveness probe."""
    return {"status": "alive", "timestamp": int(status.HTTP_200_OK)}


@router.get(
    "/readiness",
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
    description="Validates if the container is ready to serve traffic by querying PostgreSQL connectivity.",
)
async def check_readiness(
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """Verifies backend database is ready to accept queries."""
    db_check = await SystemDiagnostics.ping_database(db)
    if db_check["status"] == "healthy":
        return {"status": "ready", "database": "online"}
    return {"status": "not_ready", "database": "offline"}


@router.get(
    "/diagnostics",
    status_code=status.HTTP_200_OK,
    summary="Deep System Diagnostics",
    description="Deep diagnostic probe querying storage sizing, system loads, and database latencies.",
)
async def fetch_diagnostics(
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """Triggers deep diagnostics probing metrics."""
    return await SystemDiagnostics.run_diagnostics(db)
