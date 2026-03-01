"""Tests for Challenge 058: Cross-Reference Docs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from answers import (
    endpoint_that_writes_to_users,
    env_var_for_database_host,
    tables_accessed_by_orders_endpoint,
    port_for_production,
    endpoints_requiring_auth,
    max_connections_env_var,
    table_for_audit_logs,
    cache_ttl_for_products,
)


def test_endpoint_that_writes_to_users():
    result = endpoint_that_writes_to_users()
    assert result == "POST /api/users"


def test_env_var_for_database_host():
    assert env_var_for_database_host() == "DB_HOST"


def test_tables_accessed_by_orders_endpoint():
    result = tables_accessed_by_orders_endpoint()
    expected = ["audit_logs", "order_items", "orders", "products"]
    assert result == expected


def test_port_for_production():
    assert port_for_production() == 443


def test_endpoints_requiring_auth():
    result = endpoints_requiring_auth()
    expected = [
        "GET /api/orders",
        "GET /api/products",
        "GET /api/users",
        "POST /api/orders",
        "POST /api/users",
    ]
    assert result == expected


def test_max_connections_env_var():
    assert max_connections_env_var() == "DB_MAX_CONNECTIONS"


def test_table_for_audit_logs():
    assert table_for_audit_logs() == "audit_logs"


def test_cache_ttl_for_products():
    assert cache_ttl_for_products() == 300
