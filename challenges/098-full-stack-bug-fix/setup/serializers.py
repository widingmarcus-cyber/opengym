def serialize_order(order):
    """Convert order to dict for API response."""
    return {
        "id": order.id,
        "user_id": order.user_id,
        "items": [
            {
                "product": item.product,
                "quantity": item.quantity,
                "line_total": item.price,
            }
            for item in order.items
        ],
        "total": order.total(),
    }


def serialize_user(user):
    """Convert user to dict for API response."""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }
