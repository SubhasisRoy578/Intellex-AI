from typing import List, Dict, Any, Optional
from app.orchestrator.schemas import CitationInfo


class CitationManager:
    """Consolidates and generates uniform citations from multiple active sources (Web, Document, and OCR)."""

    @staticmethod
    def compile_citations(
        web_results: Optional[List[Dict[str, Any]]] = None,
        processed_documents: Optional[List[Dict[str, Any]]] = None,
        processed_images: Optional[List[Dict[str, Any]]] = None,
    ) -> List[CitationInfo]:
        """Iterates over raw executed outputs and formats a unified typed list of CitationInfo models."""
        compiled_citations: List[CitationInfo] = []

        # 1. Map Web Search citations
        if web_results:
            for item in web_results:
                compiled_citations.append(
                    CitationInfo(
                        type="web",
                        title=item.get("title"),
                        url=item.get("url"),
                        snippet=item.get("snippet")
                    )
                )

        # 2. Map Document processing citations
        if processed_documents:
            for doc in processed_documents:
                compiled_citations.append(
                    CitationInfo(
                        type="document",
                        document_name=doc.get("document_name"),
                        page_number=doc.get("pages")
                    )
                )

        # 3. Map OCR citations
        if processed_images:
            for img in processed_images:
                compiled_citations.append(
                    CitationInfo(
                        type="ocr",
                        document_name=img.get("image_name"),
                        snippet=f"Image processed via OCR ({img.get('width')}x{img.get('height')})"
                    )
                )

        return compiled_citations
