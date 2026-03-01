"""Utility functions for string manipulation."""


def slugify(text: str) -> str:
    """Convert a string into a URL-friendly slug.

    Lowercases the text, replaces spaces with hyphens, and removes
    non-alphanumeric characters (except hyphens).

    Args:
        text: The input string to slugify.

    Returns:
        A URL-friendly slug string.
    """
    slug = text.lower().replace(" ", "-")
    return "".join(c for c in slug if c.isalnum() or c == "-")


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to a maximum length, appending a suffix if truncated.

    Args:
        text: The input string.
        max_length: The maximum allowed length including the suffix.
        suffix: The string to append when truncation occurs.

    Returns:
        The truncated string with suffix, or the original if within limits.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def word_count(text: str) -> dict[str, int]:
    """Count the occurrences of each word in a text.

    Words are compared case-insensitively. Punctuation is stripped
    from word boundaries.

    Args:
        text: The input text to analyze.

    Returns:
        A dictionary mapping lowercase words to their counts.
    """
    counts: dict[str, int] = {}
    for word in text.lower().split():
        cleaned = word.strip(".,!?;:\"'()-")
        if cleaned:
            counts[cleaned] = counts.get(cleaned, 0) + 1
    return counts
