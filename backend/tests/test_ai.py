import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.ai.utils import estimate_token_count

client = TestClient(app)


def test_ai_health() -> None:
    """Test that the AI health endpoint reports healthy status."""
    response = client.get("/api/v1/chat/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["provider"] == "mock"
    assert json_data["default_model"] == "mock-model"


def test_chat_unauthenticated() -> None:
    """Test that calling the chat endpoint without bearer token is rejected with HTTP 401."""
    payload = {"message": "Hello Intellex AI!"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 401


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_chat_authenticated_success(mock_verify) -> None:
    """Test that a valid authenticated request processes chat prompts correctly."""
    # Mock authentication
    mock_verify.return_value = {
        "sub": "user_2g9Klx8hF7P",
        "email": "testuser@intellex.ai",
        "sid": "sess_8nVu2x6h",
    }

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"message": "Hello there!"}
    
    response = client.post("/api/v1/chat", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert "response" in json_data
    assert "conversation_id" in json_data
    assert "timestamp" in json_data
    assert json_data["provider"] == "mock"
    assert json_data["model"] == "mock-model"
    assert json_data["tokens_used"] > 0
    # Predefined mock keyword greeting check
    assert "Hello! I am Intellex AI" in json_data["response"]


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_chat_continuation(mock_verify) -> None:
    """Test that continuing an existing conversation uses and preserves the same conversation ID."""
    mock_verify.return_value = {
        "sub": "user_2g9Klx8hF7P",
        "email": "testuser@intellex.ai",
        "sid": "sess_8nVu2x6h",
    }

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    first_payload = {"message": "Premium design systems"}
    
    # 1. Start session
    response1 = client.post("/api/v1/chat", json=first_payload, headers=headers)
    assert response1.status_code == 200
    id1 = response1.json()["conversation_id"]

    # 2. Continue session
    second_payload = {"message": "How do you style yourself?", "conversation_id": id1}
    response2 = client.post("/api/v1/chat", json=second_payload, headers=headers)
    assert response2.status_code == 200
    id2 = response2.json()["conversation_id"]
    
    # Assert same conversation thread ID is preserved
    assert id1 == id2


def test_token_estimation() -> None:
    """Test that the token estimation utility counts words/chars with clean boundaries."""
    assert estimate_token_count("") == 0
    assert estimate_token_count("Hello") >= 1
    # Check estimation scale matches expectations
    long_prompt = "Intellex AI premium gold design"
    assert estimate_token_count(long_prompt) > estimate_token_count("Intellex")
