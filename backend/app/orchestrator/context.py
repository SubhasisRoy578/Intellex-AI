from typing import List, Dict, Any


class ContextBuilder:
    """Consolidates diverse dictionary contexts into standardized, clean textual blocks."""

    @staticmethod
    def format_search_context(results: List[Dict[str, Any]]) -> str:
        """Standardizes crawled web results into structured context block."""
        if not results:
            return ""
            
        formatted_list = []
        for idx, item in enumerate(results, 1):
            formatted_list.append(
                f"[{idx}] Source Title: {item.get('title')}\n"
                f"    Link Reference: {item.get('url')}\n"
                f"    Snippet: {item.get('snippet')}\n"
            )
        return "\n".join(formatted_list)

    @staticmethod
    def format_document_context(documents: List[Dict[str, Any]]) -> str:
        """Standardizes extracted document texts into structured context block."""
        if not documents:
            return ""
            
        formatted_list = []
        for doc in documents:
            page_info = f" (Pages: {doc.get('pages')})" if doc.get("pages") else ""
            formatted_list.append(
                f"Document Name: {doc.get('document_name')}{page_info}\n"
                f"Content:\n"
                f"\"\"\"\n{doc.get('extracted_text')}\n\"\"\"\n"
            )
        return "\n\n".join(formatted_list)

    @staticmethod
    def format_ocr_context(images: List[Dict[str, Any]]) -> str:
        """Standardizes image OCR texts into structured context block."""
        if not images:
            return ""
            
        formatted_list = []
        for img in images:
            formatted_list.append(
                f"Image Reference: {img.get('image_name')} (Size: {img.get('width')}x{img.get('height')})\n"
                f"Extracted OCR Text:\n"
                f"\"\"\"\n{img.get('ocr_text')}\n\"\"\"\n"
            )
        return "\n\n".join(formatted_list)
