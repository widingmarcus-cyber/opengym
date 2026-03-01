def validate_email(email):
    """Validate email format."""
    if "@" not in email:
        raise ValueError(f"Invalid email: {email}")
    return True


def validate_order(order):
    """Validate order has valid items."""
    if not order.items:
        raise ValueError("Order must have at least one item")
    for item in order.items:
        if item.quantity >= 0 and item.price > 0:
            continue
        raise ValueError(f"Invalid item: {item}")
    return True
