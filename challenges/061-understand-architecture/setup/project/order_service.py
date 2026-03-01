"""Order business logic service."""

from order_repository import OrderRepository
from product_repository import ProductRepository
from user_service import UserService
from order_model import Order, OrderItem


class OrderService:
    def __init__(self, order_repo=None, product_repo=None, user_service=None):
        self.order_repo = order_repo or OrderRepository()
        self.product_repo = product_repo or ProductRepository()
        self.user_service = user_service or UserService()

    def place_order(self, user_id, items):
        user = self.user_service.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        order_items = []
        for item in items:
            product = self.product_repo.find_by_id(item["product_id"])
            if not product or not product.is_available():
                raise ValueError(f"Product {item['product_id']} unavailable")
            order_items.append(
                OrderItem(product.product_id, item["quantity"], product.price)
            )

        order_id = len(self.order_repo.find_all()) + 1
        order = Order(order_id, user_id, order_items)
        return self.order_repo.save(order)

    def get_order(self, order_id):
        order = self.order_repo.find_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        return order

    def get_user_orders(self, user_id):
        return self.order_repo.find_by_user(user_id)

    def cancel_order(self, order_id):
        order = self.get_order(order_id)
        if not order.cancel():
            raise ValueError("Cannot cancel order")
        return order
