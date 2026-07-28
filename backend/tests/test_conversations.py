import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models.conversation import Conversation
from app.conversations.service import conversation_service
from app.conversations.cleanup import ConversationCleanupService

client = TestClient(app)


def test_conversations_health() -> None:
    """Test that the conversations module health reports correctly."""
    response = client.get("/api/v1/conversations/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["retention_limit_per_user"] == 10


def test_conversations_unauthenticated() -> None:
    """Test that list conversations without bearer token is rejected with HTTP 401."""
    response = client.get("/api/v1/conversations")
    assert response.status_code == 401


@patch("app.auth.clerk.clerk_verifier.verify_token")
@patch("app.conversations.routes.conversation_service.create_new_conversation")
def test_create_conversation_success(mock_create, mock_verify) -> None:
    """Test creating a new conversation successfully scoped to active authenticated user."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    
    # Mock return value as Conversation DB model
    mock_thread = Conversation(
        id="conv_uuid_123",
        user_id="user_2g9Klx8hF7P",
        title="My Premium Chat",
        message_count=0,
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        last_activity_at=datetime.now(timezone.utc),
        messages=[]
    )
    mock_create.return_value = mock_thread

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"title": "My Premium Chat"}

    response = client.post("/api/v1/conversations", json=payload, headers=headers)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["id"] == "conv_uuid_123"
    assert json_data["title"] == "My Premium Chat"
    assert json_data["message_count"] == 0


@patch("app.auth.clerk.clerk_verifier.verify_token")
@patch("app.conversations.routes.conversation_service.list_user_threads")
def test_list_conversations_success(mock_list, mock_verify) -> None:
    """Test listing user conversations paginated results successfully."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    
    # Mock items list
    now = datetime.now(timezone.utc)
    mock_items = [
        Conversation(
            id="conv_1", user_id="user_2g9Klx8hF7P", title="Chat 1", message_count=2, status="active",
            created_at=now, updated_at=now, last_activity_at=now, messages=[]
        ),
        Conversation(
            id="conv_2", user_id="user_2g9Klx8hF7P", title="Chat 2", message_count=1, status="archived",
            created_at=now, updated_at=now, last_activity_at=now, messages=[]
        )
    ]
    mock_list.return_value = (2, mock_items)

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    response = client.get("/api/v1/conversations?page=1&limit=5", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["total"] == 2
    assert len(json_data["items"]) == 2
    assert json_data["items"][0]["id"] == "conv_1"
    assert json_data["items"][1]["status"] == "archived"


@patch("app.auth.clerk.clerk_verifier.verify_token")
@patch("app.conversations.routes.conversation_service.calculate_user_statistics")
def test_conversations_stats(mock_stats, mock_verify) -> None:
    """Test retrieving correct user conversation metrics summaries."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    mock_stats.return_value = {
        "total_conversations": 5,
        "active_conversations": 4,
        "archived_conversations": 1,
        "total_messages": 15,
        "average_messages_per_conversation": 3.0
    }

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    response = client.get("/api/v1/conversations/stats", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["total_conversations"] == 5
    assert json_data["active_conversations"] == 4
    assert json_data["average_messages_per_conversation"] == 3.0


@pytest.mark.asyncio
async def test_retention_limiter_pruning() -> None:
    """Test that the retention cleanup service automatically deletes the oldest conversation when exceeding 10 limit."""
    # 1. Create a mocked AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    
    # 2. Mock execute queries return values
    mock_count_res = MagicMock()
    # Simulate count is 11 (meaning excess of 1 thread needs to be pruned)
    mock_count_res.scalar_or_none.return_value = 11
    
    mock_oldest_res = MagicMock()
    # Mock a list of oldest conversations
    now = datetime.now(timezone.utc)
    oldest_thread = Conversation(
        id="oldest_conv_id",
        user_id="user_2g",
        title="Oldest Thread",
        last_activity_at=now - timedelta(days=10)
    )
    mock_oldest_res.scalars.return_value.all.return_value = [oldest_thread]
    
    mock_db.execute.side_effect = [mock_count_res, mock_oldest_res]

    # 3. Trigger retention check
    pruned_count = await ConversationCleanupService.enforce_retention_limit(
        mock_db,
        user_id="user_2g",
        limit_max=10
    )

    # Assert 1 oldest conversation was successfully deleted
    assert pruned_count == 1
    mock_db.delete.assert_called_once_with(oldest_thread)
