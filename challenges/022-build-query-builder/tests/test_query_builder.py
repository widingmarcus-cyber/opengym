"""Tests for Challenge 022: Build Query Builder."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from query_builder import Query


def test_simple_select_all():
    sql = Query().table("users").build()
    assert sql == "SELECT * FROM users"


def test_select_specific_columns():
    sql = Query().table("users").select("name", "email").build()
    assert sql == "SELECT name, email FROM users"


def test_where_clause():
    sql = Query().table("users").where("age > 18").build()
    assert sql == "SELECT * FROM users WHERE age > 18"


def test_multiple_where_clauses():
    sql = (
        Query()
        .table("products")
        .where("price > 100")
        .where("in_stock = 1")
        .build()
    )
    assert sql == "SELECT * FROM products WHERE price > 100 AND in_stock = 1"


def test_order_by_default_asc():
    sql = Query().table("users").order_by("name").build()
    assert sql == "SELECT * FROM users ORDER BY name ASC"


def test_order_by_desc():
    sql = Query().table("users").order_by("created_at", "DESC").build()
    assert sql == "SELECT * FROM users ORDER BY created_at DESC"


def test_limit():
    sql = Query().table("users").limit(10).build()
    assert sql == "SELECT * FROM users LIMIT 10"


def test_offset():
    sql = Query().table("users").limit(10).offset(20).build()
    assert sql == "SELECT * FROM users LIMIT 10 OFFSET 20"


def test_full_query():
    sql = (
        Query()
        .table("users")
        .select("name", "email")
        .where("age > 18")
        .order_by("name")
        .limit(10)
        .offset(5)
        .build()
    )
    assert sql == "SELECT name, email FROM users WHERE age > 18 ORDER BY name ASC LIMIT 10 OFFSET 5"


def test_no_table_raises():
    with pytest.raises(ValueError):
        Query().select("name").build()
