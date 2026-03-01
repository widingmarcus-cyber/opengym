"""Text processing module for reading and manipulating text files."""


def read_file(filepath):
    """Read a text file and return its contents as a string.

    Args:
        filepath: str path to the file

    Returns:
        str: file contents
    """
    with open(filepath, "r", encoding="ascii") as f:
        return f.read()


def count_characters(text):
    """Return the number of characters in the text.

    Args:
        text: str

    Returns:
        int: character count (not byte count)
    """
    return len(text.encode("utf-8"))


def reverse_text(text):
    """Reverse the text character by character.

    Args:
        text: str

    Returns:
        str: reversed text
    """
    encoded = text.encode("utf-8")
    reversed_bytes = encoded[::-1]
    return reversed_bytes.decode("utf-8", errors="replace")


def extract_words(text):
    """Split text into words, stripping punctuation from each word.

    Args:
        text: str

    Returns:
        list of str: words with punctuation stripped
    """
    import string
    words = text.split()
    result = []
    for word in words:
        cleaned = word.strip(string.punctuation)
        if cleaned:
            result.append(cleaned)
    return result


def truncate(text, max_chars):
    """Truncate text to max_chars characters, adding '...' if truncated.

    Args:
        text: str
        max_chars: int

    Returns:
        str: truncated text
    """
    encoded = text.encode("utf-8")
    if len(encoded) <= max_chars:
        return text
    return encoded[:max_chars].decode("utf-8", errors="ignore") + "..."
