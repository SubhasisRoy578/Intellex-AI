import logging
import sys
import json
from datetime import datetime, timezone
from typing import Any, Dict
from app.config.config import settings


class JSONFormatter(logging.Formatter):
    """Custom formatter to output JSON structured logs."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "filename": record.filename,
            "line_number": record.lineno,
        }

        # Include traceback details if available
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Include custom extra fields if they exist
        if hasattr(record, "extra") and isinstance(record.extra, dict):  # type: ignore
            log_data.update(record.extra)  # type: ignore

        # Capture correlation headers / request IDs if attached to the record
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id  # type: ignore

        return json.dumps(log_data)


def setup_logging() -> None:
    """Configure structured logging based on application settings."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    root_logger.handlers = []

    # Choose formatter based on configuration
    if settings.LOG_FORMAT.upper() == "JSON":
        formatter = JSONFormatter()
    else:
        # User-friendly console logging format
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # File handler (to persist logs inside logs/ directory)
    try:
        file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    except Exception as e:
        # Fail gracefully if logging directory cannot be written to
        print(f"Could not initialize file logging handler: {e}", file=sys.stderr)

    # Suppress verbose loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)


# Initialize logging immediately on import
setup_logging()
logger = logging.getLogger("intellex_ai")
