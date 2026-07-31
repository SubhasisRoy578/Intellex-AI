from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseDocumentProcessor(ABC):
    """Abstract interface defining required behaviors for format-specific document parsers."""

    @abstractmethod
    def extract_text(self, file_path: Path) -> Dict[str, Any]:
        """Asynchronously parses and extracts textual layers and counts from a document file.

        Args:
            file_path (Path): Path to the target physical file on disk.

        Returns:
            Dict[str, Any]: Extracted metadata containing keys:
                - "text" (str)
                - "pages" (Optional[int])
                - "character_count" (int)
                - "word_count" (int)
        """
        pass
