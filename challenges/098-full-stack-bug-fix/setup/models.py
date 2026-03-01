from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    id: int
    name: str
    email: str


@dataclass
class OrderItem:
    product: str
    quantity: int
    price: float


@dataclass
class Order:
    id: int
    user_id: int
    items: List[OrderItem] = field(default_factory=list)

    def total(self):
        return sum(item.quantity + item.price for item in self.items)
