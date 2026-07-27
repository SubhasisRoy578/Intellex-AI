import pytest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.config.config import settings
from app.orchestrator.decision import DecisionEngine

client = TestClient(app)


def test_orchestrator_health() -> None:
    """Test that the orchestrator health endpoint reports correctly."""
    response = client.get("/api/v1/orchestrator/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert len(json_data["active_sources"]) == 4


def test_orchestrator_unauthenticated() -> None:
    """Test that querying orchestrator chat without bearer token is rejected with HTTP 401."""
    payload = {"message": "How does Intellex AI compile web searches?"}
    response = client.post("/api/v1/orchestrator/chat", json=payload)
    assert response.status_code == 401


def test_decision_engine_intent() -> None:
    """Test that the DecisionEngine detects intents based on alphanumeric keyword matches."""
    # 1. Plain chat only
    decision1 = DecisionEngine.detect_intents("Hello, how are you?")
    assert decision1["use_chat"] is True
    assert decision1["use_web"] is False
    assert decision1["use_documents"] is False

    # 2. Web search trigger
    decision2 = DecisionEngine.detect_intents("What is the latest price of gold today?")
    assert decision2["use_web"] is True

    # 3. Document/OCR trigger
    decision3 = DecisionEngine.detect_intents("Summarize this", document_upload_ids=["id1"], image_upload_ids=["id2"])
    assert decision3["use_documents"] is True
    assert decision3["use_ocr"] is True


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_orchestrated_chat_success(mock_verify) -> None:
    """Test successful joint document + search orchestrated pipeline with accurate citations."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}

    # 1. Create a dummy txt file dynamically for document source reference
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    txt_filename = "test_orchestration_doc.txt"
    txt_path = upload_dir / txt_filename
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("Intellex AI uses clean architecture backend models.")

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {
        "message": "What is the latest news on Intellex AI?",
        "document_upload_ids": [txt_filename],
    }

    # 2. Query orchestrated endpoint (triggers search intent 'latest/news' + document reference)
    response = client.post("/api/v1/orchestrator/chat", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert "response" in json_data
    assert "web_search" in json_data["knowledge_sources_used"]
    assert "document" in json_data["knowledge_sources_used"]
    assert json_data["confidence_score"] > 0.85
    
    # Assert unified citations are compiled correctly
    assert len(json_data["citations"]) > 0
    citation_types = [c["type"] for c in json_data["citations"]]
    assert "web" in citation_types
    assert "document" in citation_types

    # Cleanup
    if txt_path.exists():
        txt_path.unlink()
