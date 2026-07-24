import os
import pytest
from pathlib import Path
import fitz  # PyMuPDF
import docx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.config.config import settings
from app.documents.service import document_service
from app.documents.exceptions import PasswordProtectedException, DocumentCorruptedException

client = TestClient(app)


def test_documents_health() -> None:
    """Test that the documents module health reports correctly."""
    response = client.get("/api/v1/documents/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert ".pdf" in json_data["supported_formats"]
    assert len(json_data["libraries_active"]) > 0


def test_process_unauthenticated() -> None:
    """Test that processing a document without authentication is rejected with HTTP 401."""
    payload = {"upload_id": "non_existent_file.pdf"}
    response = client.post("/api/v1/documents/process", json=payload)
    assert response.status_code == 401


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_process_txt_success(mock_verify) -> None:
    """Test parsing and validating a stored plain text file successfully."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    
    # 1. Create a dummy plain text file in the uploads directory
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    txt_filename = "test_extraction.txt"
    txt_path = upload_dir / txt_filename
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("Hello Intellex AI!\n\nThis is a standard UTF-8 text file parsing test.")

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"upload_id": txt_filename}
    
    # 2. Process
    response = client.post("/api/v1/documents/process", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "processed"
    assert json_data["file_type"] == ".txt"
    assert json_data["character_count"] > 0
    assert json_data["word_count"] > 0
    assert "UTF-8" in json_data["extracted_text"]

    # Cleanup
    if txt_path.exists():
        txt_path.unlink()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_process_pdf_success(mock_verify) -> None:
    """Test parsing a real generated PDF file successfully using PyMuPDF (fitz)."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}

    # 1. Create a tiny valid PDF file dynamically
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    pdf_filename = "test_extraction.pdf"
    pdf_path = upload_dir / pdf_filename

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Premium Gold Intellex AI Assistant PDF Test.")
    doc.save(pdf_path)
    doc.close()

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"upload_id": pdf_filename}

    # 2. Process
    response = client.post("/api/v1/documents/process", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "processed"
    assert json_data["file_type"] == ".pdf"
    assert json_data["pages"] == 1
    assert "Premium Gold" in json_data["extracted_text"]

    # Cleanup
    if pdf_path.exists():
        pdf_path.unlink()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_process_docx_success(mock_verify) -> None:
    """Test parsing a real generated DOCX file successfully using python-docx."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}

    # 1. Create a tiny DOCX dynamically
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    docx_filename = "test_extraction.docx"
    docx_path = upload_dir / docx_filename

    doc = docx.Document()
    doc.add_paragraph("This is paragraph text in word format.")
    doc.save(docx_path)

    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"upload_id": docx_filename}

    # 2. Process
    response = client.post("/api/v1/documents/process", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "processed"
    assert json_data["file_type"] == ".docx"
    assert "paragraph text" in json_data["extracted_text"]

    # Cleanup
    if docx_path.exists():
        docx_path.unlink()


@patch("app.auth.clerk.clerk_verifier.verify_token")
def test_process_missing_file(mock_verify) -> None:
    """Test processing a non-existent upload ID returns HTTP 400."""
    mock_verify.return_value = {"sub": "user_2g9Klx8hF7P"}
    headers = {"Authorization": "Bearer mock-valid-jwt-token"}
    payload = {"upload_id": "does_not_exist_file.txt"}

    response = client.post("/api/v1/documents/process", json=payload, headers=headers)
    assert response.status_code == 400
    json_data = response.json()
    assert "could not be located" in json_data["error"]["message"].lower()
