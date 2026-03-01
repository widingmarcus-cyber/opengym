"""Hidden tests for Challenge 050: Build Test Fixture."""

import sys
import os
import importlib
import inspect
import subprocess
from pathlib import Path

# Add setup/ to path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

SETUP_DIR = Path(__file__).parent.parent / "setup"


def _reload_module(name):
    """Import and reload a module by name."""
    mod = importlib.import_module(name)
    importlib.reload(mod)
    return mod


def test_fixtures_create_sample_users():
    """Fixtures must provide create_sample_users returning at least 3 users."""
    fixtures = _reload_module("fixtures")
    assert hasattr(fixtures, "create_sample_users"), (
        "fixtures.py must define create_sample_users()"
    )
    users = fixtures.create_sample_users()
    assert isinstance(users, list), "create_sample_users must return a list"
    assert len(users) >= 3, f"Expected at least 3 users, got {len(users)}"
    for user in users:
        assert hasattr(user, "id"), "Each user must have an 'id' attribute"
        assert hasattr(user, "name"), "Each user must have a 'name' attribute"
        assert hasattr(user, "email"), "Each user must have an 'email' attribute"


def test_fixtures_create_sample_products():
    """Fixtures must provide create_sample_products returning at least 3 products."""
    fixtures = _reload_module("fixtures")
    assert hasattr(fixtures, "create_sample_products"), (
        "fixtures.py must define create_sample_products()"
    )
    products = fixtures.create_sample_products()
    assert isinstance(products, list), "create_sample_products must return a list"
    assert len(products) >= 3, f"Expected at least 3 products, got {len(products)}"
    for product in products:
        assert hasattr(product, "id"), "Each product must have an 'id' attribute"
        assert hasattr(product, "name"), "Each product must have a 'name' attribute"
        assert hasattr(product, "price"), "Each product must have a 'price' attribute"
        assert product.price > 0, "Product price must be positive"


def test_fixtures_create_populated_db():
    """Fixtures must provide create_populated_db returning a pre-loaded db."""
    fixtures = _reload_module("fixtures")
    assert hasattr(fixtures, "create_populated_db"), (
        "fixtures.py must define create_populated_db()"
    )
    db = fixtures.create_populated_db()
    assert hasattr(db, "get"), "Populated DB must have a 'get' method"
    assert hasattr(db, "insert"), "Populated DB must have an 'insert' method"
    assert hasattr(db, "query"), "Populated DB must have a 'query' method"

    users = fixtures.create_sample_users()
    for user in users:
        found = db.get("users", user.id)
        assert found is not None, f"User {user.id} should be in the populated db"

    products = fixtures.create_sample_products()
    for product in products:
        found = db.get("products", product.id)
        assert found is not None, f"Product {product.id} should be in the populated db"


def test_fixtures_create_sample_order():
    """Fixtures must provide create_sample_order that creates a valid order."""
    fixtures = _reload_module("fixtures")
    assert hasattr(fixtures, "create_sample_order"), (
        "fixtures.py must define create_sample_order(db)"
    )
    db = fixtures.create_populated_db()
    order = fixtures.create_sample_order(db)
    assert hasattr(order, "id"), "Order must have an 'id' attribute"
    assert hasattr(order, "user_id"), "Order must have a 'user_id' attribute"
    assert hasattr(order, "product_ids"), "Order must have a 'product_ids' attribute"
    assert hasattr(order, "total"), "Order must have a 'total' attribute"

    user = db.get("users", order.user_id)
    assert user is not None, "Order user_id must reference a valid user in the db"

    assert len(order.product_ids) > 0, "Sample order must have at least one product"
    assert order.total > 0, "Sample order total must be positive"


def test_test_orders_exist():
    """test_orders.py must define at least 6 test functions."""
    test_orders = _reload_module("test_orders")
    test_fns = [n for n in dir(test_orders) if n.startswith("test_")]
    assert len(test_fns) >= 6, (
        f"Expected at least 6 test functions in test_orders.py, found {len(test_fns)}: {test_fns}"
    )


def test_test_orders_use_fixtures():
    """test_orders.py must import and use fixtures from fixtures.py."""
    test_orders = _reload_module("test_orders")
    source = inspect.getsource(test_orders)
    assert "fixtures" in source or "fixture" in source, (
        "test_orders.py must import and use fixtures from fixtures.py"
    )


def test_test_orders_pass():
    """All agent-written tests in test_orders.py must pass."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test_orders.py", "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=str(SETUP_DIR),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert result.returncode == 0, (
        f"Agent tests in test_orders.py failed:\n{result.stdout}\n{result.stderr}"
    )


def test_order_total_uses_product_prices():
    """Verify that the agent's fixtures compute order totals from product prices."""
    fixtures = _reload_module("fixtures")
    db = fixtures.create_populated_db()
    order = fixtures.create_sample_order(db)

    expected_total = 0.0
    for pid in order.product_ids:
        product = db.get("products", pid)
        assert product is not None, f"Product {pid} in order should exist in db"
        expected_total += product.price

    assert abs(order.total - expected_total) < 0.01, (
        f"Order total {order.total} should match sum of product prices {expected_total}"
    )
