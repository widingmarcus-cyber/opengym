"""Data processor that transforms items and caches results."""

from cache import add_to_cache, get_cache, clear_cache


def process_items(items):
    """Process a list of items: double each value and cache the results.

    Args:
        items: List of numbers to process

    Returns:
        List of processed (doubled) values
    """
    clear_cache()
    results = []
    for item in items:
        processed = item * 2
        add_to_cache(processed)
        results.append(processed)
    return results


def get_processed_count():
    """Return the number of items currently in the cache."""
    return len(get_cache())


def get_processed_items():
    """Return a copy of all processed items in the cache."""
    return list(get_cache())
