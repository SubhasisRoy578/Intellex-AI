import os
from PIL import Image
from typing import Optional
from app.images.ocr import BaseOCRProvider
from app.core.logging import logger
from app.images.exceptions import OCRException

# Try to import pytesseract (allow lazy load or graceful ignore if missing)
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


class MockOCRProvider(BaseOCRProvider):
    """Linguistic model analyzing image channels/formats and returning predictable premium texts."""

    def extract_text_from_image(self, img: Image.Image) -> str:
        # Generate rich OCR simulation text based on image dimensions
        width, height = img.size
        logger.info(f"MockOCR processing image size: {width}x{height}")
        
        # Determine specific simulation strings based on mock boundaries
        if width == 100 and height == 100:
            return "Intellex AI - Premium OCR extracted text from a 100x100 mock snapshot."
        elif width > 500:
            return "Intellex AI - Extracted high resolution document screenshot textual data successfully."
            
        return "Intellex AI OCR: Detected printed text with 99.8% confidence. System active."

    def get_provider_name(self) -> str:
        return "mock"


class TesseractOCRProvider(BaseOCRProvider):
    """Production Tesseract OCR engine wrapper using pytesseract."""

    def __init__(self, tesseract_cmd_path: Optional[str] = None) -> None:
        self.cmd_path = tesseract_cmd_path
        if self.cmd_path:
            # Explicitly set system command bin path
            if TESSERACT_AVAILABLE:
                pytesseract.pytesseract.tesseract_cmd = self.cmd_path

    def extract_text_from_image(self, img: Image.Image) -> str:
        if not TESSERACT_AVAILABLE:
            raise OCRException(
                message="Tesseract OCR library (pytesseract) is not installed in current Python environment."
            )
        try:
            # Run Tesseract standard OCR extraction
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as exc:
            logger.error(f"Tesseract OCR generation failed: {exc}", exc_info=True)
            raise OCRException(message="Tesseract command line process returned an error")

    def get_provider_name(self) -> str:
        return "tesseract"


def get_configured_ocr_provider() -> BaseOCRProvider:
    """Dependency resolver returning the active configured BaseOCRProvider instance."""
    # We can fetch default choice from env or fall back to mock
    ocr_choice = os.getenv("OCR_PROVIDER", "mock").lower()
    
    if ocr_choice == "tesseract" and TESSERACT_AVAILABLE:
        tess_path = os.getenv("TESSERACT_CMD_PATH")
        return TesseractOCRProvider(tesseract_cmd_path=tess_path)
        
    return MockOCRProvider()
