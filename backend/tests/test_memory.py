import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

from app.memory.models import Memory
from app.memory.schemas import MemoryCreate, MemoryUpdate
from app.memory.ranking import MemoryRanker
from app.memory.retriever import MemoryRetriever
from app.memory.exceptions import MemoryNotFoundException, MemoryForbiddenException

client = TestClient(app)


def test_memory_ranker_relevance_keywords() -> None:
    """Test MemoryRanker correctly scores keyword similarity matches."""
    mem = Memory(
        id="mem-1",
        user_id="user-123",
        category="preferences",
        title="FastAPI Web Framework",
        content="I prefer building RESTful backends with Python and FastAPI because of Pydantic and clean typing.",
        importance_score=0.8,
        tags="python,fastapi",
        is_active=True
    )

    query_tokens = {"python", "fastapi"}
    score_with_keywords = MemoryRanker.calculate_relevance_score(mem, query_tokens)

    query_tokens_empty = set()
    score_without_keywords = MemoryRanker.calculate_relevance_score(mem, query_tokens_empty)

    # Keywords matching should provide a significantly higher score
    assert score_with_keywords > score_without_keywords


def test_memory_ranker_tag_boost() -> None:
    """Test MemoryRanker applies tag boosts to score alignment."""
    mem = Memory(
        id="mem-2",
        user_id="user-123",
        category="projects",
        title="Intellex AI",
        content="Building an automated agent.",
        importance_score=0.5,
        tags="agent,intellex",
        is_active=True
    )

    query_tokens = {"building"}
    score_no_tags = MemoryRanker.calculate_relevance_score(mem, query_tokens, query_tags=set())
    score_with_tags = MemoryRanker.calculate_relevance_score(mem, query_tokens, query_tags={"agent"})

    assert score_with_tags > score_no_tags


def test_memory_ranker_ranking() -> None:
    """Test MemoryRanker ranks memory records correctly in descending order."""
    m1 = Memory(id="1", user_id="u", category="c", title="Flask", content="Flask info", importance_score=0.2, tags="", is_active=True)
    m2 = Memory(id="2", user_id="u", category="c", title="FastAPI Framework", content="FastAPI backend python", importance_score=0.9, tags="", is_active=True)

    ranked = MemoryRanker.rank_memories([m1, m2], query="FastAPI python", limit=5)
    assert len(ranked) == 2
    # m2 should rank first due to higher importance score and matching title/content keywords
    assert ranked[0][0].id == "2"


def test_memory_retriever_formatting() -> None:
    """Test serialization of memories into structured XML context tags."""
    memories = [
        Memory(id="m1", user_id="u1", category="preferences", title="Theme", content="Dark theme", importance_score=0.5, is_active=True),
        Memory(id="m2", user_id="u1", category="projects", title="Work", content="Building backend", importance_score=0.6, is_active=True)
    ]
    formatted = MemoryRetriever.format_context_for_prompt(memories)
    assert "<PREFERENCES" in formatted
    assert "Dark theme" in formatted
    assert "<PROJECTS" in formatted
    assert "Building backend" in formatted


@patch("app.auth.clerk.clerk_verifier.verify_token")
@patch("app.memory.service.MemoryService.create_memory")
def test_create_memory_authenticated(mock_create, mock_verify) -> None:
    """Test creating a memory record successfully with valid Bearer authentication."""
    mock_verify.return_value = {"sub": "user_123456"}

    mock_record = Memory(
        id="mem-uuid-999",
        user_id="user_123456",
        category="preferences",
        title="Custom Preference",
        content="Likes dark mode.",
        importance_score=0.7,
        source="user",
        tags="profile",
        is_active=True
    )
    mock_create.return_value = mock_record

    headers = {"Authorization": "Bearer mock-token-123"}
    payload = {
        "category": "preferences",
        "title": "Custom Preference",
        "content": "Likes dark mode.",
        "importance_score": 0.7,
        "source": "user",
        "tags": "profile",
        "is_active": True
    }

    response = client.post("/api/v1/memories", json=payload, headers=headers)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["id"] == "mem-uuid-999"
    assert json_data["user_id"] == "user_123456"
    assert json_data["category"] == "preferences"
    assert json_data["title"] == "Custom Preference"


def test_memory_unauthenticated_rejected() -> None:
    """Test that requests to list memories without authorization headers are rejected."""
    response = client.get("/api/v1/memories")
    assert response.status_code == 401


@patch("app.auth.clerk.clerk_verifier.verify_token")
@patch("app.memory.service.MemoryService.list_memories")
def test_list_memories_authenticated(mock_list, mock_verify) -> None:
    """Test listing user memories works correctly and supports filtering parameters."""
    mock_verify.return_value = {"sub": "user_123456"}

    mock_record = Memory(
        id="mem-1",
        user_id="user_123456",
        category="preferences",
        title="Testing",
        content="Content info",
        importance_score=0.5,
        source="user",
        tags="test",
        is_active=True
    )
    mock_list.return_value = (1, [mock_record])

    headers = {"Authorization": "Bearer mock-token-123"}
    response = client.get("/api/v1/memories?category=preferences&limit=5", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["total"] == 1
    assert len(json_data["items"]) == 1
    assert json_data["items"][0]["id"] == "mem-1"


@patch("app.auth.clerk.clerk_verifier.verify_token")
@patch("app.memory.service.MemoryService.retrieve_metrics")
def test_memory_stats(mock_stats, mock_verify) -> None:
    """Test retrieving user-specific memory analytics and category metadata."""
    mock_verify.return_value = {"sub": "user_123456"}
    mock_stats.return_value = {
        "total_memories": 10,
        "active_memories": 8,
        "categories": [
            {"category": "preferences", "count": 5},
            {"category": "projects", "count": 3}
        ]
    }

    headers = {"Authorization": "Bearer mock-token-123"}
    response = client.get("/api/v1/memories/stats", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["total_memories"] == 10
    assert json_data["active_memories"] == 8
    assert len(json_data["categories"]) == 2
