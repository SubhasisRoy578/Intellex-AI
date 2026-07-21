import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Test that the API root endpoint responds successfully with general info."""
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"
    assert "app_name" in json_data
    assert "version" in json_data


def test_health_check_endpoint() -> None:
    """Test that the health check endpoint responds successfully."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert "services" in json_data
    assert "api" in json_data["services"]
    assert "database" in json_data["services"]
    assert json_data["services"]["api"]["status"] == "healthy"
