import re
from typing import List, Dict, Any


class CitationBuilder:
    """Manages web resource deduplication, citation key indexing, and quality ranking filters."""

    @staticmethod
    def deduplicate_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters out duplicate URLs based on canonical domain/path matching.

        Args:
            results (List[Dict[str, Any]]): Raw unverified results.

        Returns:
            List[Dict[str, Any]]: Deduplicated results list.
        """
        seen_urls = set()
        unique_results = []

        for item in results:
            url = item.get("url", "").strip()

            # Normalize url (strip protocol and trailing slashes/hashes)
            norm_url = re.sub(r"^(https?://)?(www\.)?", "", url).lower().rstrip("/")

            if norm_url and norm_url not in seen_urls:
                seen_urls.add(norm_url)
                unique_results.append(item)

        return unique_results

    @staticmethod
    def rank_and_sort(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sorts search results by relevance rank score descending."""
        return sorted(results, key=lambda x: x.get("score", 0.0), reverse=True)
