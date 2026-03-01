"""Order data model."""

from datetime import datetime


class OrderItem:
    def __init__(self, product_id, quantity, unit_price):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def subtotal(self):
        return self.quantity * self.unit_price


class Order:
    def __init__(self, order_id, user_id, items=None):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items or []
        self.status = "pending"
        self.created_at = datetime.now()

    def total(self):
        return sum(item.subtotal() for item in self.items)

    def to_dict(self):
        return {
            "id": self.order_id,
            "user_id": self.user_id,
            "status": self.status,
            "total": self.total(),
            "items": len(self.items),
            "created_at": self.created_at.isoformat(),
        }

    def cancel(self):
        if self.status == "pending":
            self.status = "cancelled"
            return True
        return False
