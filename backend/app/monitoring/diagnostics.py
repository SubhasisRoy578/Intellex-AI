import os
import shutil
import time
from pathlib import Path
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import settings
from app.core.logging import logger


class SystemDiagnostics:
    """Provides liveness, readiness, database connectivity, and physical storage diagnostics probes."""

    @staticmethod
    async def ping_database(db: AsyncSession) -> Dict[str, Any]:
        """Probes and measures PostgreSQL connection latency."""
        start = time.perf_counter()
        try:
            await db.execute(text("SELECT 1"))
            latency_ms = (time.perf_counter() - start) * 1000
            return {
                "status": "healthy",
                "latency": f"{latency_ms:.2f}ms"
            }
        except Exception as exc:
            logger.error(f"Diagnostics: Database connectivity check failed: {exc}")
            return {
                "status": "unhealthy",
                "error": str(exc)
            }

    @staticmethod
    def probe_storage_capacity() -> Dict[str, Any]:
        """Validates that local uploads and log storage sizing does not exceed limit targets (450 MB)."""
        uploads_dir = Path(settings.UPLOAD_DIR)
        logs_dir = Path("logs")

        # Sum total sizes
        total_bytes = 0
        for directory in [uploads_dir, logs_dir]:
            if directory.exists():
                for f in directory.rglob("*"):
                    if f.is_file():
                        total_bytes += f.stat().st_size

        total_mb = total_bytes / (1024 * 1024)
        target_max_mb = settings.MAX_STORAGE_TARGET_MB

        return {
            "current_size_bytes": total_bytes,
            "current_size_mb": f"{total_mb:.2f} MB",
            "target_limit_mb": f"{target_max_mb} MB",
            "capacity_status": "optimal" if total_mb < target_max_mb else "warn_limit_exceeded"
        }

    @classmethod
    async def run_diagnostics(cls, db: AsyncSession) -> Dict[str, Any]:
        """Runs complete deep diagnostics probing."""
        db_probe = await cls.ping_database(db)
        storage_probe = cls.probe_storage_capacity()

        overall_status = "healthy"
        if db_probe["status"] == "unhealthy" or storage_probe["capacity_status"] != "optimal":
            overall_status = "degraded"

        return {
            "status": overall_status,
            "timestamp": time.time(),
            "diagnostics": {
                "database": db_probe,
                "storage": storage_probe,
                "ai_engine": {
                    "provider": settings.AI_PROVIDER,
                    "default_model": settings.AI_DEFAULT_MODEL
                }
            }
        }
