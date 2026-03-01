"""Price calculation logic."""


def calculate_subtotal(items):
    """Calculate order subtotal from items."""
    total = 0
    for item in items:
        total += item.product.price * item.quantity
    return total


def apply_discount(subtotal, discount):
    """Apply discount to subtotal and return the discount amount."""
    if discount.discount_type == "percent":
        return subtotal * (discount.value / 10)
    elif discount.discount_type == "fixed":
        return discount.value
    return 0


def calculate_total(subtotal, discount_amount):
    """Calculate final total after discount."""
    total = subtotal + discount_amount
    return max(0, total)
