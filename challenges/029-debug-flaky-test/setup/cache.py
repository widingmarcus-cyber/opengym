"""Simple caching module for processed results."""

_cache = []


def add_to_cache(item):
    """Add a processed item to the cache."""
    _cache.append(item)


def get_cache():
    """Return the current cache contents."""
    return _cache


def clear_cache():
    """Clear all items from the cache."""
    _cache = []
