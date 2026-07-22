import math


def estimate_token_count(text: str) -> int:
    """Estimates the number of tokens in a text block using standard split metrics.

    Linguistic standard: ~4 characters per token or ~0.75 words per token.

    Args:
        text (str): Input text string.

    Returns:
        int: Approximated token count (guaranteed minimum of 1 for non-empty text).
    """
    if not text:
        return 0
        
    word_count = len(text.split())
    char_count = len(text)
    
    # Take the average of both split models for improved approximation accuracy
    token_est_from_words = math.ceil(word_count / 0.75)
    token_est_from_chars = math.ceil(char_count / 4.0)
    
    avg_tokens = math.ceil((token_est_from_words + token_est_from_chars) / 2)
    return max(1, avg_tokens)
