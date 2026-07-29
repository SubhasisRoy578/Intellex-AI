import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.cache import cache_service

client = TestClient(app)


def test_monitoring_liveness() -> None:
    """Test that liveness probe returns correct status indicators."""
    response = client.get("/api/v1/monitoring/liveness")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "alive"


def test_monitoring_readiness() -> None:
    """Test that readiness probe responds correctly."""
    response = client.get("/api/v1/monitoring/readiness")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data


def test_monitoring_diagnostics() -> None:
    """Test that the diagnostics probe returns comprehensive metrics logs."""
    response = client.get("/api/v1/monitoring/diagnostics")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert "diagnostics" in json_data
    assert "database" in json_data["diagnostics"]
    assert "storage" in json_data["diagnostics"]


def test_cache_service() -> None:
    """Test the in-memory cache operations with key sets, fetches, and expirations."""
    cache_service.clear()
    
    # 1. Standard set and get
    cache_service.set("test_key", "IntellexAI", ttl=5)
    assert cache_service.get("test_key") == "IntellexAI"

    # 2. Expiration (TTL = 0 seconds)
    cache_service.set("exp_key", "ExpiredVal", ttl=0)
    # Artificially sleep or wait
    time.sleep(0.01)
    assert cache_service.get("exp_key") is None

    # 3. Explicit delete
    cache_service.set("del_key", "DeleteMe")
    cache_service.delete("del_key")
    assert cache_service.get("del_key") is None


def test_security_headers() -> None:
    """Test that strict production security headers are injected into HTTP responses."""
    response = client.get("/")
    assert response.status_code == 200
    headers = response.headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Strict-Transport-Security" in headers
    assert "Content-Security-Policy" in headers


def test_rate_limiting_enforcement() -> None:
    """Test that making excessive requests triggers rate limiting rejections (HTTP 429)."""
    # Force mock rate limiter capacity bounds to small threshold (e.g. 2 requests per minute)
    with patch("app.middleware.rate_limit.settings.RATE_LIMIT_PER_MINUTE", 2):
        # We need a clean limiter instance for the mock threshold to reflect
        limiter = app.user_middleware[2].kwargs["app"] # Locate rate limit middleware instance if needed
        
        # Dispatch 3 quick requests to root index
        responses = [client.get("/") for _ in range(4)]
        
        status_codes = [r.status_code for r in responses]
        assert 429 in status_codes
