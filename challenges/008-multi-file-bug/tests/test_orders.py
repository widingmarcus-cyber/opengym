"""Tests for Challenge 008: Multi-File Bug Hunt."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from app.models import Product, OrderItem
from app.orders import process_order


def make_items():
    """Helper: Create a standard order of $100."""
    return [
        OrderItem(product=Product("Widget", 25.0), quantity=2),  # $50
        OrderItem(product=Product("Gadget", 50.0), quantity=1),  # $50
    ]  # Total: $100


def test_no_discount():
    """Order without discount code should have full price."""
    items = make_items()
    order = process_order(items)
    assert order.subtotal == 100.0
    assert order.discount_amount == 0
    assert order.total == 100.0


def test_percent_discount():
    """SAVE20 = 20% off $100 = $20 discount = $80 total."""
    items = make_items()
    order = process_order(items, "SAVE20")
    assert order.subtotal == 100.0
    assert order.discount_amount == 20.0
    assert order.total == 80.0


def test_fixed_discount():
    """FLAT10 = $10 off $100 = $90 total."""
    items = make_items()
    order = process_order(items, "FLAT10")
    assert order.subtotal == 100.0
    assert order.discount_amount == 10.0
    assert order.total == 90.0


def test_half_off():
    """HALF = 50% off $100 = $50 total."""
    items = make_items()
    order = process_order(items, "HALF")
    assert order.subtotal == 100.0
    assert order.discount_amount == 50.0
    assert order.total == 50.0


def test_discount_case_insensitive():
    """Discount codes should work regardless of case."""
    items = make_items()
    order = process_order(items, "save20")
    assert order.discount_amount == 20.0
    assert order.total == 80.0


def test_discount_min_order_not_met():
    """Discount should not apply if order is below minimum."""
    items = [OrderItem(product=Product("Small", 10.0), quantity=1)]  # $10
    order = process_order(items, "FLAT10")  # min_order=25
    assert order.discount_amount == 0
    assert order.total == 10.0


def test_invalid_discount_code():
    """Invalid code should result in no discount."""
    items = make_items()
    order = process_order(items, "NOTREAL")
    assert order.discount_amount == 0
    assert order.total == 100.0


def test_total_never_negative():
    """Total should never go below zero."""
    items = [OrderItem(product=Product("Tiny", 3.0), quantity=1)]  # $3
    order = process_order(items, "FIVER")  # $5 off, min_order=0
    assert order.total == 0  # Not -2
