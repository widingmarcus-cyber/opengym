"""Order repository for data access."""

from order_model import Order


class OrderRepository:
    def __init__(self):
        self._orders = {}

    def save(self, order):
        self._orders[order.order_id] = order
        return order

    def find_by_id(self, order_id):
        return self._orders.get(order_id)

    def find_by_user(self, user_id):
        return [o for o in self._orders.values() if o.user_id == user_id]

    def find_all(self):
        return list(self._orders.values())

    def find_by_status(self, status):
        return [o for o in self._orders.values() if o.status == status]

    def delete(self, order_id):
        return self._orders.pop(order_id, None)
