import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from models import Order, OrderItem, User
from validators import validate_email, validate_order
from serializers import serialize_order, serialize_user
from api import register_user, create_order


# ---------------------------------------------------------------------------
# Email validation
# ---------------------------------------------------------------------------

def test_valid_email_accepted():
    assert validate_email("user@example.com") is True


def test_email_without_domain_rejected():
    with pytest.raises(ValueError):
        validate_email("user@")


def test_email_without_dot_rejected():
    with pytest.raises(ValueError):
        validate_email("user@domain")


# ---------------------------------------------------------------------------
# Order model and validation
# ---------------------------------------------------------------------------

def test_valid_order_total():
    order = Order(
        id=1,
        user_id=1,
        items=[
            OrderItem(product="Widget", quantity=2, price=10.0),
            OrderItem(product="Gadget", quantity=3, price=5.0),
        ],
    )
    assert order.total() == 35.0


def test_negative_quantity_rejected():
    order = Order(
        id=1,
        user_id=1,
        items=[OrderItem(product="Widget", quantity=-1, price=10.0)],
    )
    with pytest.raises(ValueError):
        validate_order(order)


def test_zero_quantity_rejected():
    order = Order(
        id=1,
        user_id=1,
        items=[OrderItem(product="Widget", quantity=0, price=10.0)],
    )
    with pytest.raises(ValueError):
        validate_order(order)


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def test_serialized_line_total():
    order = Order(
        id=1,
        user_id=1,
        items=[OrderItem(product="Widget", quantity=4, price=7.5)],
    )
    result = serialize_order(order)
    assert result["items"][0]["line_total"] == 30.0


# ---------------------------------------------------------------------------
# Full API flows
# ---------------------------------------------------------------------------

def test_full_registration_flow():
    result = register_user(1, "Alice", "alice@example.com")
    assert result == {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
    }


def test_full_order_flow():
    items = [{"product": "Widget", "quantity": 2, "price": 10.0}]
    result = create_order(1, 1, items)
    assert result["total"] == 20.0
    assert result["items"][0]["line_total"] == 20.0


def test_order_multiple_items():
    items = [
        {"product": "Widget", "quantity": 2, "price": 10.0},
        {"product": "Gadget", "quantity": 1, "price": 25.0},
        {"product": "Doohickey", "quantity": 5, "price": 3.0},
    ]
    result = create_order(1, 1, items)
    assert result["items"][0]["line_total"] == 20.0
    assert result["items"][1]["line_total"] == 25.0
    assert result["items"][2]["line_total"] == 15.0
    assert result["total"] == 60.0
