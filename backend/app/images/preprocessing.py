from PIL import Image, ImageEnhance, ImageOps
from pathlib import Path
from app.core.logging import logger
from app.images.exceptions import ImageCorruptedException


class ImagePreprocessor:
    """Provides high-quality, lightweight image preprocessing operations to prepare images for OCR."""

    @staticmethod
    def preprocess_for_ocr(
        img: Image.Image,
        enhance_contrast: bool = True,
        enhance_brightness: bool = True,
        convert_grayscale: bool = True
    ) -> Image.Image:
        """Applies brightness, contrast, and grayscale enhancements on PIL images.

        Args:
            img (PIL.Image.Image): Raw PIL image.
            enhance_contrast (bool): Triggers contrast boost.
            enhance_brightness (bool): Triggers brightness boost.
            convert_grayscale (bool): Triggers grayscale conversion.

        Returns:
            PIL.Image.Image: Preprocessed, clean image.
        """
        processed_img = img.copy()

        # 1. Automatic Rotation alignment based on EXIF tags
        try:
            processed_img = ImageOps.exif_transpose(processed_img)
        except Exception as exc:
            logger.warning(f"Could not perform EXIF transposition alignment: {exc}")

        # 2. Convert to Grayscale
        if convert_grayscale:
            try:
                processed_img = processed_img.convert("L")
            except Exception as exc:
                logger.error(f"Failed converting image to grayscale: {exc}")

        # 3. Enhance Contrast (boost thresholding)
        if enhance_contrast:
            try:
                enhancer = ImageEnhance.Contrast(processed_img)
                processed_img = enhancer.enhance(1.5)  # Boost contrast by 50%
            except Exception as exc:
                logger.error(f"Failed contrast enhancement: {exc}")

        # 4. Enhance Brightness (adjust lighting conditions)
        if enhance_brightness:
            try:
                enhancer = ImageEnhance.Brightness(processed_img)
                processed_img = enhancer.enhance(1.1)  # Slightly boost brightness by 10%
            except Exception as exc:
                logger.error(f"Failed brightness enhancement: {exc}")

        return processed_img
