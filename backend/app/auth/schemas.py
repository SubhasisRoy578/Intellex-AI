from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ClerkUser(BaseModel):
    """User profile metadata extracted and validated from Clerk authentication JWT."""
    
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier of the user (e.g. sub claim)")
    email: Optional[str] = Field(None, description="Email address associated with the Clerk user")
    session_id: Optional[str] = Field(None, description="Clerk active session identifier")
    raw_payload: dict = Field(default_factory=dict, description="Raw dictionary representation of the token claims")


class AuthHealthSchema(BaseModel):
    """Authentication API health validation model."""

    status: str = Field(..., description="Reporting of Clerk Auth functionality status")
    clerk_issuer: str = Field(..., description="Configured Clerk JWT issuer")
