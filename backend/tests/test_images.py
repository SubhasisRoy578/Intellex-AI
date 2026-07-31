import os
import pytest
from pathlib import Path
from PIL import Image
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.config.config import settings

client = TestClient(app)


def test_images_health() -> None:
    """Test that the images module health reports correctly."""
    response = client.get("/api/v1/images/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["ocr_provider"] == "mock"
    assert ".png" in json_data["supported_formats"]


def test_process_unauthenticated() -> None:
    """Test that processing an image without authentication is rejected with HTTP 401."""
    payload = {"upload_id": "non_existent_image.png"}
    response = client.post("/api/v1/images/process", json=payload)
    assert response.status_code == 401


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_process_image_success(mock_verify) -> None:
    """Test parsing and running OCR on a real generated PNG file successfully using Pillow and MockOCR."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}

    # 1. Create a tiny valid PNG image dynamically inside the uploads directory
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    img_filename = "test_ocr_snapshot.png"
    img_path = upload_dir / img_filename

    # Create 100x100 dummy blue image
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(img_path)

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"upload_id": img_filename}

    # 2. Process
    response = client.post("/api/v1/images/process", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "processed"
    assert json_data["width"] == 100
    assert json_data["height"] == 100
    assert json_data["format"] == "PNG"
    assert json_data["file_size"] > 0
    # Our mock OCR return special strings for 100x100 dimensions
    assert "mock snapshot" in json_data["ocr_text"]

    # Cleanup
    if img_path.exists():
        img_path.unlink()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_process_missing_image(mock_verify) -> None:
    """Test processing a non-existent image upload ID returns HTTP 400."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"upload_id": "does_not_exist_image.png"}

    response = client.post("/api/v1/images/process", json=payload, headers=headers)
    assert response.status_code == 400
    json_data = response.json()
    assert "could not be located" in json_data["error"]["message"].lower()
