from typing import Any, Dict, Optional
from app.auth.schemas import ClerkUser
from app.core.logging import logger


class AuthService:
    """Service to handle user context processing and optional local synchronization."""

    @staticmethod
    def sync_user_session(clerk_user: ClerkUser) -> Optional[Dict[str, Any]]:
        """Synchronizes and logs user session context locally.

        This service can be expanded in the future to register users inside the local
        PostgreSQL database when they authenticate for the first time.
        """
        logger.info(
            f"Auth session synchronized for user: {clerk_user.id}",
            extra={"extra": {"user_id": clerk_user.id, "email": clerk_user.email}}
        )
        return {
            "user_id": clerk_user.id,
            "email": clerk_user.email,
            "synced": True
        }


auth_service = AuthService()
