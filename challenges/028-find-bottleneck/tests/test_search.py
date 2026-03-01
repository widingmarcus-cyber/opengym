"""Tests for Challenge 028: Find the Bottleneck."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from search import build_index, search, search_by_category


PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics"},
    {"id": 2, "name": "Wireless Keyboard", "category": "Electronics"},
    {"id": 3, "name": "USB Cable", "category": "Accessories"},
    {"id": 4, "name": "Mouse Pad", "category": "Accessories"},
    {"id": 5, "name": "Monitor Stand", "category": "Furniture"},
    {"id": 6, "name": "Desk Lamp", "category": "Furniture"},
    {"id": 7, "name": "Laptop Bag", "category": "Accessories"},
    {"id": 8, "name": "Bluetooth Speaker", "category": "Electronics"},
    {"id": 9, "name": "Phone Case", "category": "Accessories"},
    {"id": 10, "name": "Webcam", "category": "Electronics"},
]


def test_index_is_not_plain_list():
    """build_index must create an efficient lookup structure, not just wrap the list."""
    index = build_index(PRODUCTS)
    # The index should contain lookup structures, not just {"products": [...]}
    # Check that it's not simply storing the raw product list
    if isinstance(index, dict):
        values = list(index.values())
        has_only_product_list = (
            len(values) == 1 and isinstance(values[0], list)
            and len(values[0]) == len(PRODUCTS)
        )
        assert not has_only_product_list, (
            "build_index just wraps the product list — no index was built. "
            "Create a lookup structure (e.g., dict keyed by name tokens or category)."
        )


def test_search_returns_correct_results():
    """Basic search returns the right products."""
    index = build_index(PRODUCTS)
    results = search(index, "Mouse")
    names = [r["name"] for r in results]
    assert "Wireless Mouse" in names
    assert "Mouse Pad" in names
    assert len(results) == 2


def test_search_case_insensitive():
    """Search should be case-insensitive."""
    index = build_index(PRODUCTS)
    results_lower = search(index, "wireless")
    results_upper = search(index, "WIRELESS")
    assert len(results_lower) == len(results_upper) == 2


def test_search_no_results():
    """Search with no matches returns empty list."""
    index = build_index(PRODUCTS)
    results = search(index, "Toaster")
    assert results == []


def test_search_partial_match():
    """Search should match partial strings."""
    index = build_index(PRODUCTS)
    results = search(index, "Lap")
    names = [r["name"] for r in results]
    assert "Laptop Bag" in names


def test_search_by_category():
    """Category search returns all products in that category."""
    index = build_index(PRODUCTS)
    results = search_by_category(index, "electronics")
    assert len(results) == 4
    for r in results:
        assert r["category"] == "Electronics"


def test_search_performance():
    """Search must complete 10000 lookups in under 1 second.

    This requires an efficient data structure, not a linear scan.
    """
    large_catalog = []
    for i in range(5000):
        large_catalog.append({
            "id": i,
            "name": f"Product {i} Alpha",
            "category": "General",
        })
    large_catalog.append({
        "id": 9999,
        "name": "Target Widget",
        "category": "Special",
    })

    index = build_index(large_catalog)

    start = time.time()
    for _ in range(10000):
        results = search(index, "Target Widget")
    elapsed = time.time() - start

    assert len(results) == 1
    assert results[0]["name"] == "Target Widget"
    assert elapsed < 1.0, f"Search took {elapsed:.2f}s for 10000 queries (must be < 1s)"


def test_build_index_has_category_keys():
    """The index should have entries keyed by category for fast lookup."""
    index = build_index(PRODUCTS)
    if isinstance(index, dict):
        # If it's a dict, it should have category names as keys — not just "products"
        has_category_keys = any(
            key.lower() in ("electronics", "accessories", "furniture")
            for key in index.keys()
        )
        has_only_products_key = list(index.keys()) == ["products"]
        assert has_category_keys or not has_only_products_key, (
            f"build_index returns a dict with only key(s) {list(index.keys())}. "
            "A proper index should map category names to product lists for fast lookup."
        )


def test_search_by_category_does_not_iterate_all():
    """search_by_category should use the index, not iterate all products."""
    import inspect
    source = inspect.getsource(search_by_category)
    # The buggy version iterates over index["products"] — a full linear scan
    scans_all = ('index["products"]' in source or "index['products']" in source)
    assert not scans_all, (
        "search_by_category iterates over index['products'] — this is a linear scan. "
        "It should use the index structure to look up products by category directly."
    )


def test_build_index_groups_products():
    """build_index should group products by some key for O(1) lookup."""
    index = build_index(PRODUCTS)
    if isinstance(index, dict):
        # A good index has multiple keys (one per category or per term)
        # A bad index has just 1 key with all products dumped in
        assert len(index) > 1, (
            f"build_index returns a dict with {len(index)} key(s): {list(index.keys())}. "
            "An effective index should have multiple entries for fast lookup."
        )


def test_category_search_performance():
    """Category search must also be efficient on large catalogs."""
    large_catalog = []
    for i in range(5000):
        large_catalog.append({
            "id": i,
            "name": f"Product {i}",
            "category": f"Cat{i % 50}",
        })

    index = build_index(large_catalog)

    start = time.time()
    for _ in range(10000):
        results = search_by_category(index, "Cat0")
    elapsed = time.time() - start

    assert len(results) == 100  # 5000/50 = 100 per category
    assert elapsed < 1.0, f"Category search took {elapsed:.2f}s for 10000 queries (must be < 1s)"
