"""Utility functions module."""

import re


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text


def truncate(text, max_len, suffix="..."):
    """Truncate text to max_len characters, appending suffix if truncated."""
    if len(text) <= max_len:
        return text
    return text[:max_len - len(suffix)] + suffix


def is_valid_url(url):
    """Return True if the string is a valid HTTP or HTTPS URL."""
    pattern = re.compile(
        r'^https?://'
        r'[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*'
        r'(:\d+)?'
        r'(/[^\s]*)?$'
    )
    return bool(pattern.match(url))


def deep_merge(dict_a, dict_b):
    """Deep merge two dictionaries. Values in dict_b take precedence."""
    result = dict_a.copy()
    for key, value in dict_b.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def chunk_list(lst, size):
    """Split a list into chunks of the given size."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i:i + size] for i in range(0, len(lst), size)]
