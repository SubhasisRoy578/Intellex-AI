from typing import Optional
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.clerk import clerk_verifier
from app.auth.schemas import ClerkUser
from app.auth.exceptions import MissingTokenException, InvalidTokenException

# Declare standard HTTPBearer scheme, allowing auto OpenAPI swagger mapping
security_scheme = HTTPBearer(auto_error=False)


def parse_bearer_token(credentials: Optional[HTTPAuthorizationCredentials]) -> str:
    """Parses and extracts the token from HTTP Bearer credentials.

    Args:
        credentials (Optional[HTTPAuthorizationCredentials]): Security bearer object.

    Returns:
        str: Raw JWT token.
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        raise MissingTokenException(message="Missing or invalid Bearer authentication credentials")
    
    token = credentials.credentials.strip()
    if not token:
        raise MissingTokenException(message="Authorization Bearer token is empty")
    
    return token


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)
) -> ClerkUser:
    """Dependency to retrieve and validate the currently authenticated user.

    Strict enforcement. If the token is invalid or missing, raises exceptions.

    Returns:
        ClerkUser: Validated Clerk user info.
    """
    token = parse_bearer_token(credentials)
    payload = clerk_verifier.verify_token(token)

    # Map token claims to clean ClerkUser schema
    return ClerkUser(
        id=payload.get("sub", ""),
        email=payload.get("email") or (payload.get("emails", [None])[0] if isinstance(payload.get("emails"), list) else payload.get("emails")),
        session_id=payload.get("sid"),
        raw_payload=payload
    )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)
) -> Optional[ClerkUser]:
    """Dependency for public routes where authentication is optional.

    Returns None if missing or invalid, instead of raising error.

    Returns:
        Optional[ClerkUser]: User details if valid token is provided, else None.
    """
    try:
        if not credentials or credentials.scheme.lower() != "bearer":
            return None
            
        token = credentials.credentials.strip()
        if not token:
            return None

        payload = clerk_verifier.verify_token(token)
        return ClerkUser(
            id=payload.get("sub", ""),
            email=payload.get("email") or (payload.get("emails", [None])[0] if isinstance(payload.get("emails"), list) else payload.get("emails")),
            session_id=payload.get("sid"),
            raw_payload=payload
        )
    except Exception:
        # Silently fail for optional routes
        return None
