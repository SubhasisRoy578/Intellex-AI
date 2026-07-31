import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.search.citations import CitationBuilder

client = TestClient(app)


def test_search_health() -> None:
    """Test that the search module health reports correctly."""
    response = client.get("/api/v1/search/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["search_provider"] == "mock"


def test_search_unauthenticated() -> None:
    """Test that searching without bearer authentication is rejected with HTTP 401."""
    payload = {"query": "FastAPI clean architecture"}
    response = client.post("/api/v1/search", json=payload)
    assert response.status_code == 401


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_search_success(mock_verify) -> None:
    """Test searching with valid authentication returns accurate standardized results."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"query": "clerk jwt", "limit": 2}

    response = client.post("/api/v1/search", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["query"] == "clerk jwt"
    assert len(json_data["results"]) <= 2

    first_res = json_data["results"][0]
    assert "title" in first_res
    assert "url" in first_res
    assert "snippet" in first_res
    assert "score" in first_res
    assert first_res["source"] == "mock"


def test_citation_deduplication() -> None:
    """Test that the CitationBuilder removes duplicate URLs regardless of protocol or casing."""
    raw_results = [
        {"title": "Doc1", "url": "https://intellex.ai/page", "score": 0.9},
        {"title": "Doc2", "url": "http://intellex.ai/page/", "score": 0.8},  # Duplicate url (stripped / and protocol)
        {"title": "Doc3", "url": "https://intellex.ai/other", "score": 0.75},
    ]

    deduped = CitationBuilder.deduplicate_results(raw_results)
    assert len(deduped) == 2
    assert deduped[0]["title"] == "Doc1"
    assert deduped[1]["title"] == "Doc3"
