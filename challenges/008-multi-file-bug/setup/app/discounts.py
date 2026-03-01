"""Discount code lookup and validation."""

from app.models import Discount

# Available discount codes
DISCOUNTS = {
    "SAVE20": Discount(code="SAVE20", discount_type="percent", value=20, min_order=50),
    "FLAT10": Discount(code="FLAT10", discount_type="fixed", value=10, min_order=25),
    "HALF": Discount(code="HALF", discount_type="percent", value=50, min_order=100),
    "FIVER": Discount(code="FIVER", discount_type="fixed", value=5, min_order=0),
}


def lookup_discount(code):
    """Look up a discount by code. Returns Discount or None."""
    return DISCOUNTS.get(code)


def validate_discount(discount, subtotal):
    """Check if a discount is valid for the given subtotal."""
    if discount is None:
        return False
    if subtotal < discount.min_order:
        return False
    return True
