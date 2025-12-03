"""Simple tools for text analysis that can be used by agents."""

import re
from typing import List
from langchain_core.tools import tool


@tool
def count_words(text: str) -> dict:
    """
    Count the number of words, characters, and sentences in the given text.

    Args:
        text: The text to analyze

    Returns:
        Dictionary with word_count, char_count, and sentence_count
    """
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    # Simple sentence detection - split by common sentence endings
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])

    return {
        "word_count": word_count,
        "character_count": char_count,
        "sentence_count": sentence_count,
    }


@tool
def extract_keywords(text: str, n: int = 5) -> dict:
    """
    Extract the most common keywords from the text.

    Args:
        text: The text to analyze
        n: Number of keywords to extract (default: 5)

    Returns:
        Dictionary with keywords and their frequencies
    """
    # Simple keyword extraction - remove common stop words
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "must", "can", "this",
        "that", "these", "those", "i", "you", "he", "she", "it", "we", "they"
    }

    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter out stop words and short words
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 3]

    # Count frequencies
    word_freq = {}
    for word in meaningful_words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # Get top N keywords
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    top_keywords = dict(sorted_keywords[:n])

    return {
        "keywords": top_keywords,
        "total_unique_keywords": len(word_freq),
    }


def get_tools() -> List:
    """
    Get all available tools as a list.

    Returns:
        List of tool instances
    """
    return [count_words, extract_keywords]

