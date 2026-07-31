from abc import ABC, abstractmethod
from PIL import Image


class BaseOCRProvider(ABC):
    """Abstract base interface defining behaviors for interchangeable OCR text extraction engines."""

    @abstractmethod
    def extract_text_from_image(self, img: Image.Image) -> str:
        """Asynchronously or synchronously runs text extraction on a preprocessed PIL Image.

        Args:
            img (PIL.Image.Image): Preprocessed PIL image.

        Returns:
            str: Extracted clean text string.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the active registered name of this OCR engine (e.g. 'mock', 'tesseract')."""
        pass
