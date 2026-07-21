import jwt
from typing import Any, Dict, Optional
from app.config.config import settings
from app.core.logging import logger
from app.auth.exceptions import InvalidTokenException, ExpiredTokenException


class ClerkJWTVerifier:
    """Clerk JWT validation utility utilizing local RS256 JWKS public keys decryption."""

    def __init__(self) -> None:
        self.issuer = settings.CLERK_JWT_ISSUER
        # JWKS URI endpoint under Clerk accounts domain
        self.jwks_url = f"{self.issuer.rstrip('/')}/.well-known/jwks.json"
        self._jwks_client: Optional[jwt.PyJWKClient] = None

    @property
    def jwks_client(self) -> jwt.PyJWKClient:
        """Lazy initializer for PyJWKClient to avoid hitting network on application start."""
        if self._jwks_client is None:
            self._jwks_client = jwt.PyJWKClient(self.jwks_url)
        return self._jwks_client

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Decodes, verifies the signature, and validates claims for a Clerk JWT.

        Args:
            token (str): JWT string.

        Returns:
            Dict[str, Any]: Decoded payload dictionary.
        """
        try:
            # Dynamically fetch the signing public key from Clerk JWKS cache
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            
            # Decode the token, validating signature, expiration (exp), and issuer (iss)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                options={"verify_aud": False}, # Clerk JWTs usually omit audience claim
            )
            return payload
            
        except jwt.ExpiredSignatureError as e:
            logger.warning(f"Clerk Token expired: {e}")
            raise ExpiredTokenException(message="Authentication token has expired")
            
        except jwt.InvalidIssuerError as e:
            logger.warning(f"Clerk Token issuer mismatch: {e}")
            raise InvalidTokenException(message="Token issuer verification failed")
            
        except (jwt.InvalidSignatureError, jwt.DecodeError) as e:
            logger.warning(f"Clerk Token signature/decode validation failed: {e}")
            raise InvalidTokenException(message="Signature verification failed")
            
        except Exception as e:
            logger.error(f"Unexpected error during Clerk JWT validation: {e}", exc_info=True)
            raise InvalidTokenException(message="Could not decode authentication token")


# Shared instance
clerk_verifier = ClerkJWTVerifier()
