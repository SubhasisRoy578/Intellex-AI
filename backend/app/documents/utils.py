import re
import unicodedata


def clean_extracted_text(text: str) -> str:
    """Performs structured text cleaning and normalization on parsed documents.

    Args:
        text (str): Raw extracted document string.

    Returns:
        str: Cleansed and standardized string.
    """
    if not text:
        return ""

    # 1. Unicode Normalization (NFKC compat form)
    normalized = unicodedata.normalize("NFKC", text)

    # 2. Strip non-printable control characters (except common linebreaks and tab formatters)
    clean_text = "".join(ch for ch in normalized if ch == "\n" or ch == "\r" or ch == "\t" or not unicodedata.category(ch).startswith("C"))

    # 3. Collapse multiple consecutive empty lines to maintain readability but save footprint
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)

    return clean_text.strip()
