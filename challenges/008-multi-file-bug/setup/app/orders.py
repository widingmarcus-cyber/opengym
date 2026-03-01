"""Order processing — entry point."""

from app.models import Order, OrderItem
from app.discounts import lookup_discount, validate_discount
from app.pricing import calculate_subtotal, apply_discount, calculate_total


def process_order(items, discount_code=""):
    """Process an order with optional discount code.

    Args:
        items: list of OrderItem
        discount_code: optional discount code string

    Returns:
        Order object with calculated subtotal, discount, and total
    """
    order = Order(items=items, discount_code=discount_code)
    order.subtotal = calculate_subtotal(items)

    discount_amount = 0
    if discount_code:
        discount = lookup_discount(discount_code)
        if discount and validate_discount(discount, order.subtotal):
            discount_amount = apply_discount(order.subtotal, discount)

    order.discount_amount = discount_amount
    order.total = calculate_total(order.subtotal, discount_amount)

    return order
