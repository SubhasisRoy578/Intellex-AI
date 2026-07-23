import io
import os
import time
import pytest
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.config.config import settings
from app.uploads.service import storage_service, LocalStorageProvider
from app.uploads.validators import sanitize_filename

client = TestClient(app)


def test_uploads_health() -> None:
    """Test that the uploads health endpoint reports correctly."""
    response = client.get("/api/v1/uploads/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["storage_provider"] == "local"
    assert json_data["max_file_size_bytes"] == settings.MAX_UPLOAD_SIZE


def test_upload_unauthenticated() -> None:
    """Test that uploading a file without bearer authentication is rejected with HTTP 401."""
    files = {"file": ("test_doc.pdf", b"Some dummy content", "application/pdf")}
    response = client.post("/api/v1/uploads", files=files)
    assert response.status_code == 401


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_upload_authenticated_success(mock_verify) -> None:
    """Test uploading a valid PDF document with successful authentication."""
    mock_verify.return_value = {
        "sub": "user_2g9Klx8hF7P",
        "email": "testuser@intellex.ai",
        "sid": "sess_8nVu2x6h",
    }

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    files = {"file": ("test_doc.pdf", b"Some premium document content", "application/pdf")}
    
    response = client.post("/api/v1/uploads", files=files, headers=headers)
    assert response.status_code == 201
    json_data = response.json()
    assert "upload_id" in json_data
    assert json_data["original_filename"] == "test_doc.pdf"
    assert json_data["file_type"] == ".pdf"
    assert json_data["file_size"] > 0
    assert json_data["upload_status"] == "stored"

    # Cleanup the stored file from disk
    stored_name = json_data["stored_filename"]
    target_path = Path(settings.UPLOAD_DIR) / stored_name
    if target_path.exists():
        target_path.unlink()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_upload_invalid_extension(mock_verify) -> None:
    """Test uploading a file with an unsupported extension is rejected with HTTP 400."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    files = {"file": ("forbidden.exe", b"Some executable code", "application/octet-stream")}

    response = client.post("/api/v1/uploads", files=files, headers=headers)
    assert response.status_code == 400
    json_data = response.json()
    assert "extension" in json_data["error"]["message"].lower()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_upload_empty_file(mock_verify) -> None:
    """Test uploading an empty file is rejected with HTTP 400."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    files = {"file": ("empty.txt", b"", "text/plain")}

    response = client.post("/api/v1/uploads", files=files, headers=headers)
    assert response.status_code == 400
    json_data = response.json()
    assert "empty" in json_data["error"]["message"].lower()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_upload_too_large(mock_verify) -> None:
    """Test uploading a file exceeding max size bounds is rejected with HTTP 413."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    
    # Prepare dummy massive content exceeding settings.MAX_UPLOAD_SIZE (e.g. 11MB)
    large_content = b"x" * (settings.MAX_UPLOAD_SIZE + 100)
    files = {"file": ("huge.txt", large_content, "text/plain")}

    response = client.post("/api/v1/uploads", files=files, headers=headers)
    assert response.status_code == 413
    json_data = response.json()
    assert "exceeds" in json_data["error"]["message"].lower()


def test_sanitize_filename() -> None:
    """Test that filename sanitation strips directories path traversal and dangerous characters."""
    assert sanitize_filename("../../../dangerous_file.pdf") == "dangerous_file.pdf"
    assert sanitize_filename("my file#name$.docx") == "myfilename.docx"
    assert sanitize_filename("with-dash_and_underscore.png") == "with-dash_and_underscore.png"


def test_automatic_cleanup() -> None:
    """Test that LocalStorageProvider's automatic cleanup prunes files older than age bounds."""
    # Write a test file in upload dir
    test_provider = LocalStorageProvider(storage_dir="test_cleanup_uploads")
    dummy_path = Path("test_cleanup_uploads") / "cleanup_test_file.txt"
    test_provider.storage_dir.mkdir(parents=True, exist_ok=True)
    
    with open(dummy_path, "wb") as f:
        f.write(b"Temp data")

    # Artificially shift access/modification times backwards by 48 hours (older than 24h limit)
    past_time = time.time() - (48 * 3600)
    os.utime(dummy_path, (past_time, past_time))

    # Run cleanup
    pruned_count = test_provider.perform_automatic_cleanup(max_age_hours=24.0)
    assert pruned_count == 1
    assert not dummy_path.exists()

    # Clear directories
    if Path("test_cleanup_uploads").exists():
        import shutil
        shutil.rmtree("test_cleanup_uploads")
