import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.auth.exceptions import InvalidTokenException, ExpiredTokenException

client = TestClient(app)


def test_auth_health() -> None:
    """Test that auth health reports correct configured issuer properties."""
    response = client.get("/api/v1/auth/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert "clerk_issuer" in json_data


def test_get_me_missing_token() -> None:
    """Test that requesting user profile without bearer token raises HTTP 401."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    json_data = response.json()
    assert json_data["success"] is False
    assert "authentication credentials" in json_data["error"]["message"].lower()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_get_me_valid_token(mock_verify) -> None:
    """Test that a valid bearer token decodes and returns the profile successfully."""
    # Setup mock decoded claims payload
    mock_verify.return_value = {
        "sub": "user_2g9Klx8hF7P",
        "email": "testuser@intellex.ai",
        "sid": "sess_8nVu2x6h",
    }

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == "user_2g9Klx8hF7P"
    assert json_data["email"] == "testuser@intellex.ai"
    assert json_data["session_id"] == "sess_8nVu2x6h"


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_get_me_expired_token(mock_verify) -> None:
    """Test that an expired token raises the ExpiredTokenException (HTTP 401)."""
    mock_verify.side_effect = ExpiredTokenException(message="Authentication token has expired")

    headers = {"Authorization": "Bearer mock-expired-jwt-token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401
    json_data = response.json()
    assert json_data["success"] is False
    assert "expired" in json_data["error"]["message"]


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_get_me_invalid_token(mock_verify) -> None:
    """Test that an invalid signature token raises InvalidTokenException (HTTP 401)."""
    mock_verify.side_effect = InvalidTokenException(message="Signature verification failed")

    headers = {"Authorization": "Bearer mock-invalid-jwt-token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401
    json_data = response.json()
    assert json_data["success"] is False
    assert "verification" in json_data["error"]["message"]
