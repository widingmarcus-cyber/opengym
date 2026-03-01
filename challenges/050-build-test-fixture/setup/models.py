"""Data models for the e-commerce system."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    id: str
    name: str
    email: str


@dataclass
class Product:
    id: str
    name: str
    price: float


@dataclass
class Order:
    id: str
    user_id: str
    product_ids: List[str] = field(default_factory=list)
    total: float = 0.0
