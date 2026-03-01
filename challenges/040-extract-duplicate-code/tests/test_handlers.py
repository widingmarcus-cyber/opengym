"""Tests for Challenge 040: Extract Duplicate Code."""

import sys
import inspect
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from handlers import handle_user, handle_product, handle_order, handle_payment
import handlers


# --- Test that original handler functions still work ---

def test_handle_user_valid():
    result = handle_user({"name": "Alice", "age": 30, "email": "ALICE@EXAMPLE.COM"})
    assert result["valid"] is True
    assert result["record"]["name"] == "Alice"
    assert result["record"]["age"] == 30
    assert result["record"]["email"] == "alice@example.com"
    assert "name=Alice" in result["summary"]


def test_handle_user_invalid():
    result = handle_user({"name": "Alice"})
    assert result["valid"] is False
    assert result["record"] is None
    assert "missing field" in result["summary"]


def test_handle_product_valid():
    result = handle_product({"title": "Widget", "price": "9.99", "quantity": "5"})
    assert result["valid"] is True
    assert result["record"]["title"] == "Widget"
    assert result["record"]["price"] == 9.99
    assert result["record"]["quantity"] == 5


def test_handle_product_invalid():
    result = handle_product({"title": "", "price": 10, "quantity": 1})
    assert result["valid"] is False
    assert result["summary"] == "validation failed"


def test_handle_order_valid():
    result = handle_order({"order_id": "ORD-001", "amount": 150.0, "status": "PENDING"})
    assert result["valid"] is True
    assert result["record"]["status"] == "pending"
    assert result["record"]["amount"] == 150.0


def test_handle_order_invalid_input():
    result = handle_order("not a dict")
    assert result["valid"] is False
    assert result["summary"] == "invalid input"


def test_handle_payment_valid():
    result = handle_payment({"payment_id": "PAY-100", "total": 75.50, "method": "CREDIT"})
    assert result["valid"] is True
    assert result["record"]["method"] == "credit"
    assert result["record"]["total"] == 75.50


def test_handle_payment_negative_total():
    result = handle_payment({"payment_id": "PAY-100", "total": -10, "method": "cash"})
    assert result["valid"] is False
    assert result["summary"] == "validation failed"


# --- Tests checking DRY: a shared helper must exist and be used ---

def test_shared_helper_exists():
    """A shared helper function must exist in the handlers module."""
    helper_names = [
        name for name, obj in inspect.getmembers(handlers, inspect.isfunction)
        if name not in ("handle_user", "handle_product", "handle_order", "handle_payment")
    ]
    assert len(helper_names) >= 1, (
        "Expected at least one shared helper function besides the four handlers. "
        f"Found only: {[n for n, _ in inspect.getmembers(handlers, inspect.isfunction)]}"
    )


def test_handlers_call_shared_helper():
    """Each handler function's source code should call the shared helper."""
    helper_names = [
        name for name, obj in inspect.getmembers(handlers, inspect.isfunction)
        if name not in ("handle_user", "handle_product", "handle_order", "handle_payment")
    ]
    assert len(helper_names) >= 1, "No shared helper found"

    helper_name = helper_names[0]

    for handler_name in ("handle_user", "handle_product", "handle_order", "handle_payment"):
        source = inspect.getsource(getattr(handlers, handler_name))
        assert helper_name in source, (
            f"{handler_name} does not appear to call the shared helper '{helper_name}'. "
            "All handlers should delegate to the shared helper to avoid duplication."
        )


def test_handlers_are_short():
    """After extracting common logic, each handler should be concise (< 10 lines)."""
    for handler_name in ("handle_user", "handle_product", "handle_order", "handle_payment"):
        source = inspect.getsource(getattr(handlers, handler_name))
        lines = [l for l in source.strip().split("\n") if l.strip() and not l.strip().startswith("#")]
        assert len(lines) <= 10, (
            f"{handler_name} has {len(lines)} non-empty lines — still too much inline logic. "
            "Extract the common validation/conversion/formatting into a shared helper."
        )


def test_no_duplicated_patterns():
    """The validation/summary pattern should not be repeated across handlers."""
    sources = []
    for handler_name in ("handle_user", "handle_product", "handle_order", "handle_payment"):
        source = inspect.getsource(getattr(handlers, handler_name))
        sources.append(source)

    # Count how many handlers contain the full inline pattern
    inline_count = 0
    for source in sources:
        # These patterns indicate inline duplication (present in original code)
        has_isinstance_check = "isinstance(data, dict)" in source
        has_for_field_loop = "for field in required" in source or "for field in" in source
        has_join_summary = "\" | \".join" in source or '"|".join' in source

        if has_isinstance_check and has_for_field_loop and has_join_summary:
            inline_count += 1

    assert inline_count <= 1, (
        f"{inline_count} handlers still have the full validation/summary pattern inline. "
        "Extract the common logic into a shared helper function."
    )


def test_total_source_lines_reduced():
    """After refactoring, handlers.py should be significantly shorter."""
    source = inspect.getsource(handlers)
    lines = [l for l in source.strip().split("\n") if l.strip() and not l.strip().startswith("#")]
    # Original is ~100 non-empty lines with duplication. After refactoring
    # with a shared helper, it should be under 70 lines.
    assert len(lines) < 70, (
        f"handlers.py has {len(lines)} non-empty lines — too much code. "
        "Extracting a shared helper should significantly reduce the line count."
    )


def test_no_repeated_try_except():
    """try/except should appear in at most one handler (the helper)."""
    count = 0
    for handler_name in ("handle_user", "handle_product", "handle_order", "handle_payment"):
        source = inspect.getsource(getattr(handlers, handler_name))
        if "except" in source and "try" in source:
            count += 1
    assert count <= 1, (
        f"{count} handlers have try/except blocks. "
        "Move the try/except logic into the shared helper."
    )


def test_no_repeated_isinstance_check():
    """isinstance(data, dict) should appear in at most one handler."""
    count = 0
    for handler_name in ("handle_user", "handle_product", "handle_order", "handle_payment"):
        source = inspect.getsource(getattr(handlers, handler_name))
        if "isinstance" in source:
            count += 1
    assert count <= 1, (
        f"{count} handlers have isinstance checks. "
        "Move input validation into the shared helper."
    )


def test_no_repeated_for_field_loop():
    """The 'for field in required' pattern should appear in at most one handler."""
    count = 0
    for handler_name in ("handle_user", "handle_product", "handle_order", "handle_payment"):
        source = inspect.getsource(getattr(handlers, handler_name))
        if "for field in" in source:
            count += 1
    assert count <= 1, (
        f"{count} handlers have 'for field in' loops. "
        "Move required-field checking into the shared helper."
    )


def test_no_repeated_summary_join():
    """The summary formatting pattern should appear in at most one handler."""
    count = 0
    for handler_name in ("handle_user", "handle_product", "handle_order", "handle_payment"):
        source = inspect.getsource(getattr(handlers, handler_name))
        if '" | ".join' in source or "' | '.join" in source:
            count += 1
    assert count <= 1, (
        f"{count} handlers have ' | '.join summary formatting. "
        "Move summary generation into the shared helper."
    )
