import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.agent.service import AgentPlanner, ToolExecutor

client = TestClient(app)


def test_agent_planner_rules() -> None:
    """Test that the AgentPlanner constructs a logical sequence of tools based on prompt keywords."""
    available = ["search", "ocr", "document_parser", "ai_chat"]

    # Test Web Search intent trigger
    plan_web = AgentPlanner.construct_plan("Search Google for FastAPI reviews", available)
    assert "search" in plan_web
    assert "ai_chat" in plan_web

    # Test OCR intent trigger
    plan_ocr = AgentPlanner.construct_plan("Read image contents and run OCR please", available)
    assert "ocr" in plan_ocr

    # Test Document intent trigger
    plan_doc = AgentPlanner.construct_plan("Analyze this pdf document", available)
    assert "document_parser" in plan_doc


@pytest.mark.asyncio
async def test_tool_executor_success() -> None:
    """Test ToolExecutor successfully invokes registered helper tools."""
    res = await ToolExecutor.invoke_tool("search", "Intellex AI")
    assert res["status"] == "success"
    assert "snippets" in res["output"]


@pytest.mark.asyncio
async def test_tool_executor_invalid_tool() -> None:
    """Test ToolExecutor fails gracefully if an unregistered tool key is provided."""
    res = await ToolExecutor.invoke_tool("non_existent_tool", "test query")
    assert res["status"] == "failed"
    assert "not registered" in res["error"]


def test_agent_health() -> None:
    """Test agent module health reports correct available tools."""
    response = client.get("/api/v1/agent/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert "search" in json_data["registered_tools"]


@patch("app.auth.clerk.clerk_verifier.verify_token")
@patch("app.orchestrator.service.OrchestratorService.execute_orchestrated_chat")
def test_agent_chat_success(mock_orchestrate, mock_verify) -> None:
    """Test initiating an autonomous agent chat flow with authenticated bearer credentials."""
    mock_verify.return_value = {"sub": "user_agent_1"}
    mock_orchestrate.return_value = {
        "response": "Hello agent! This is the unified response.",
        "tokens_used": 150,
        "citations": [],
        "knowledge_sources_used": ["web_search"],
        "confidence_score": 0.9,
        "processed_timestamp": 12345678,
        "metadata": {}
    }

    headers = {"Authorization": "Bearer mock-agent-token"}
    payload = {"message": "Please search for FastAPI reviews"}

    response = client.post("/api/v1/agent/chat", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert "unified response" in json_data["response"]
    assert len(json_data["tools_executed"]) > 0
    assert json_data["tools_executed"][0]["tool_name"] == "search"
