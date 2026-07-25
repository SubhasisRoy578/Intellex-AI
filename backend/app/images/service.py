import time
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image
from app.config.config import settings
from app.core.logging import logger
from app.images.metadata import ImageMetadataExtractor
from app.images.preprocessing import ImagePreprocessor
from app.images.ocr import BaseOCRProvider
from app.images.provider import get_configured_ocr_provider
from app.images.exceptions import ImageCorruptedException, ImageProcessingException


class ImageProcessingService:
    """Core orchestrator service coordinating the image parsing, preprocessing, and OCR text extraction."""

    def __init__(self, ocr_provider: BaseOCRProvider, upload_dir: Optional[str] = None) -> None:
        self.ocr_provider = ocr_provider
        self.upload_dir = Path(upload_dir or settings.UPLOAD_DIR)

    def process_stored_image(self, upload_id: str) -> Dict[str, Any]:
        """Loads a stored image by its filename, parses metadata, preprocesses, runs OCR, and returns analytics.

        Args:
            upload_id (str): Secure unique internal filename stored on disk.

        Returns:
            Dict[str, Any]: Map of image analytics and extracted texts.
        """
        target_path = self.upload_dir / upload_id
        
        # Security check: prevent breakout path traversal
        if not target_path.resolve().is_relative_to(self.upload_dir.resolve()):
            raise ImageProcessingException(message="Invalid image path lookup block")

        if not target_path.exists():
            logger.warning(f"Image file lookup failed for: {upload_id}")
            raise ImageCorruptedException(message="The specified image could not be located in storage")

        file_size = target_path.stat().st_size

        # 1. Extract physical dimensions and properties
        metadata = ImageMetadataExtractor.extract_metadata(target_path)
        if metadata["width"] == 0 or metadata["height"] == 0:
            raise ImageCorruptedException(message="Image file appears to be corrupted or invalid")

        logger.info(
            f"Processing image {upload_id} with OCR Engine '{self.ocr_provider.get_provider_name()}'..."
        )

        try:
            # 2. Open image in PIL
            with Image.open(target_path) as img:
                # 3. Apply high-quality contrast and grayscale preprocessing
                preprocessed_img = ImagePreprocessor.preprocess_for_ocr(img)

                # 4. Extract OCR text
                ocr_text = self.ocr_provider.extract_text_from_image(preprocessed_img)

            return {
                "status": "processed",
                "width": metadata["width"],
                "height": metadata["height"],
                "format": metadata["format"],
                "file_size": file_size,
                "ocr_text": ocr_text,
                "processed_timestamp": time.time()
            }

        except Exception as exc:
            if isinstance(exc, (ImageCorruptedException, ImageProcessingException)):
                raise exc
            logger.error(f"Failed to execute image preprocessing/OCR: {exc}", exc_info=True)
            raise ImageProcessingException(message="Internal image OCR pipeline execution failed")


# Global default instance
image_service = ImageProcessingService(ocr_provider=get_configured_ocr_provider())
