from models import User, Order, OrderItem
from validators import validate_email, validate_order
from serializers import serialize_order, serialize_user


def register_user(user_id, name, email):
    validate_email(email)
    user = User(id=user_id, name=name, email=email)
    return serialize_user(user)


def create_order(order_id, user_id, items_data):
    items = [
        OrderItem(product=i["product"], quantity=i["quantity"], price=i["price"])
        for i in items_data
    ]
    order = Order(id=order_id, user_id=user_id, items=items)
    validate_order(order)
    return serialize_order(order)
