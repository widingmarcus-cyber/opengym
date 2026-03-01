"""Order API controller."""

from order_service import OrderService
from user_service import UserService


class OrderController:
    def __init__(self, order_service=None, user_service=None):
        self.order_service = order_service or OrderService()
        self.user_service = user_service or UserService()

    def place_order(self, request):
        user_id = request["user_id"]
        user = self.user_service.get_user(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        try:
            order = self.order_service.place_order(user_id, request["items"])
            return {"status": "success", "data": order.to_dict()}
        except ValueError as e:
            return {"status": "error", "message": str(e)}

    def get_order(self, request):
        try:
            order = self.order_service.get_order(request["order_id"])
            return {"status": "success", "data": order.to_dict()}
        except ValueError as e:
            return {"status": "error", "message": str(e)}

    def cancel_order(self, request):
        try:
            order = self.order_service.cancel_order(request["order_id"])
            return {"status": "success", "data": order.to_dict()}
        except ValueError as e:
            return {"status": "error", "message": str(e)}

    def get_user_orders(self, request):
        orders = self.order_service.get_user_orders(request["user_id"])
        return {
            "status": "success",
            "data": [o.to_dict() for o in orders],
        }
