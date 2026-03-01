"""Tests for Challenge 061: Understand Architecture."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from answers import (
    what_pattern_is_used,
    list_all_services,
    what_depends_on,
    find_circular_dependencies,
    count_layers,
)


def test_what_pattern_is_used():
    assert what_pattern_is_used() == "repository"


def test_list_all_services():
    result = list_all_services()
    expected = ["OrderService", "ProductService", "UserService"]
    assert result == expected


def test_what_depends_on_order_service():
    result = what_depends_on("order_service.py")
    expected = ["order_model.py", "order_repository.py", "product_repository.py", "user_service.py"]
    assert result == expected


def test_what_depends_on_product_controller():
    result = what_depends_on("product_controller.py")
    expected = ["product_service.py"]
    assert result == expected


def test_what_depends_on_auth_middleware():
    result = what_depends_on("auth_middleware.py")
    expected = ["user_service.py"]
    assert result == expected


def test_what_depends_on_model_no_deps():
    result = what_depends_on("product_model.py")
    assert result == []


def test_find_circular_dependencies():
    result = find_circular_dependencies()
    assert len(result) == 1
    assert result[0] == ("order_service.py", "user_service.py")


def test_count_layers():
    assert count_layers() == 5
