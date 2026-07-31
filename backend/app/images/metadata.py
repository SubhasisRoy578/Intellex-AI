from PIL import Image
from pathlib import Path
from typing import Dict, Any
from app.core.logging import logger


class ImageMetadataExtractor:
    """Utility to safely extract file metadata, formats, and dimensional properties from images."""

    @staticmethod
    def extract_metadata(file_path: Path) -> Dict[str, Any]:
        """Opens the image file and reads structural properties.

        Args:
            file_path (Path): Path to physical file.

        Returns:
            Dict[str, Any]: Image properties.
        """
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                img_format = img.format or "Unknown"

                # Check for basic channel modes (e.g. RGB, RGBA, L)
                mode = img.mode

                logger.info(
                    f"Extracted image properties for {file_path.name}: {width}x{height} ({img_format})"
                )

                return {
                    "width": width,
                    "height": height,
                    "format": img_format,
                    "mode": mode,
                }
        except Exception as exc:
            logger.error(f"Failed to extract image properties for {file_path.name}: {exc}", exc_info=True)
            return {
                "width": 0,
                "height": 0,
                "format": "Unknown",
                "mode": "Unknown",
            }
