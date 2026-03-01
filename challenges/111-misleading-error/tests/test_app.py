import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from app import process_order
from utils import Item
from config import get_discount

def test_no_discount():
    items = [Item("Widget", 25.0, 2), Item("Gadget", 50.0, 1)]
    assert process_order(items) == 100.0

def test_valid_discount():
    items = [Item("Widget", 25.0, 2), Item("Gadget", 50.0, 1)]
    assert process_order(items, "SAVE10") == 90.0

def test_unknown_discount_code():
    items = [Item("Widget", 25.0, 2)]
    # Unknown codes should apply 0% discount, not crash
    result = process_order(items, "INVALID")
    assert result == 50.0

def test_another_unknown_code():
    items = [Item("Widget", 100.0, 1)]
    # Another unknown code — must not crash
    result = process_order(items, "BOGUS")
    assert result == 100.0

def test_get_discount_returns_nonnull():
    """get_discount must handle unknown codes without returning None."""
    result = get_discount("NONEXISTENT")
    assert result is not None, (
        "get_discount('NONEXISTENT') returned None — "
        "this causes crashes in apply_discount. "
        "Return a zero-discount object for unknown codes."
    )

def test_half_discount():
    items = [Item("Widget", 100.0, 1)]
    assert process_order(items, "HALF") == 50.0

def test_save20_discount():
    items = [Item("Widget", 100.0, 1)]
    assert process_order(items, "SAVE20") == 80.0

def test_empty_order():
    assert process_order([]) == 0.0

def test_unknown_code_with_multiple_items():
    """Unknown discount code with multiple items must not crash."""
    items = [Item("A", 10.0, 1), Item("B", 20.0, 2), Item("C", 5.0, 3)]
    result = process_order(items, "FOOBAR")
    assert result == 65.0

def test_empty_string_discount_code():
    """Empty string discount code should not crash."""
    items = [Item("Widget", 100.0, 1)]
    result = process_order(items, "")
    assert result == 100.0

def test_get_discount_unknown_has_percent():
    """get_discount for unknown codes must return an object with .percent attribute."""
    result = get_discount("UNKNOWN_CODE")
    assert hasattr(result, "percent"), (
        f"get_discount('UNKNOWN_CODE') returned {result} which has no .percent attribute"
    )

def test_get_discount_unknown_returns_discount_object():
    """get_discount for unknown codes must return a Discount instance, not None."""
    from config import Discount
    result = get_discount("DOES_NOT_EXIST")
    assert isinstance(result, Discount), (
        f"get_discount('DOES_NOT_EXIST') returned {type(result).__name__}, expected Discount. "
        "Unknown codes should return a Discount with 0% rather than None."
    )

def test_get_discount_unknown_has_zero_percent():
    """get_discount for unknown codes must return a discount with 0 percent."""
    result = get_discount("NOPE")
    assert result is not None, "get_discount returned None for unknown code"
    assert result.percent == 0, (
        f"get_discount('NOPE').percent = {result.percent}, expected 0"
    )
