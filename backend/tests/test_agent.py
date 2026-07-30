import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.agent.planner import AgentPlanner
from app.agent.tools import tool_registry

client = TestClient(app)


def test_agent_health() -> None:
    """Test that the agent health endpoint reports correctly."""
    response = client.get("/api/v1/agent/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert "ai_conversation" in json_data["registered_tools"]
    assert "internet_search" in json_data["registered_tools"]


def test_agent_unauthenticated() -> None:
    """Test that querying agent chat without bearer token is rejected with HTTP 401."""
    payload = {"message": "Hello agent!"}
    response = client.post("/api/v1/agent/chat", json=payload)
    assert response.status_code == 401


def test_agent_planner_execution_plan() -> None:
    """Test that the AgentPlanner generates appropriate sequential plans based on user triggers."""
    # 1. Plain conversational chat plan
    plan1 = AgentPlanner.generate_execution_plan("Tell me a story.")
    assert len(plan1) == 1
    assert plan1[0]["tool_name"] == "ai_conversation"

    # 2. Complex context + search plan
    plan2 = AgentPlanner.generate_execution_plan(
        message="Search for the latest FastAPI best practices.",
        document_upload_ids=["doc_123"]
    )
    # Expected sequential tools: document_processing -> internet_search -> knowledge_orchestration
    tool_names = [stage["tool_name"] for i, stage in enumerate(plan2)]
    assert "document_processing" in tool_names
    assert "internet_search" in tool_names
    assert "knowledge_orchestration" in tool_names


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_agent_chat_success(mock_verify) -> None:
    """Test successful agent completion running conversational loop with registered tools."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {
        "message": "Hi, tell me about your capabilities.",
    }

    # Query agent chat endpoint
    response = client.post("/api/v1/agent/chat", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert "response" in json_data
    assert len(json_data["tools_executed"]) > 0
    assert json_data["tools_executed"][0]["tool_name"] == "ai_conversation"
    assert json_data["tools_executed"][0]["status"] == "success"
