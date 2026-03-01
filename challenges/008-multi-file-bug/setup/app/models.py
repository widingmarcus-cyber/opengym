"""Data models for the order processing system."""

from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float  # price per unit in dollars


@dataclass
class OrderItem:
    product: Product
    quantity: int


@dataclass
class Discount:
    code: str
    discount_type: str  # "percent" or "fixed"
    value: float        # percentage (0-100) or fixed dollar amount
    min_order: float    # minimum order amount to apply


@dataclass
class Order:
    items: list = field(default_factory=list)
    discount_code: str = ""
    subtotal: float = 0.0
    discount_amount: float = 0.0
    total: float = 0.0
