from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user
from app.auth.schemas import ClerkUser, AuthHealthSchema
from app.config.config import settings

router = APIRouter(prefix="/auth", tags=["Clerk Authentication"])


@router.get(
    "/me",
    response_model=ClerkUser,
    status_code=status.HTTP_200_OK,
    summary="Get Authenticated User Details",
    description="Decodes, validates, and extracts validated profile claims from the client's Bearer JWT.",
)
async def get_my_profile(
    current_user: ClerkUser = Depends(get_current_user)
) -> ClerkUser:
    """Returns the parsed and validated ClerkUser model context."""
    return current_user


@router.get(
    "/health",
    response_model=AuthHealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Verify Clerk Integration Health",
    description="Validates and reports status of configured Clerk authentication details.",
)
async def check_auth_health() -> AuthHealthSchema:
    """Reports configuration values for Clerk JWT validation system."""
    return AuthHealthSchema(
        status="healthy" if settings.CLERK_JWT_ISSUER else "unconfigured",
        clerk_issuer=settings.CLERK_JWT_ISSUER
    )
