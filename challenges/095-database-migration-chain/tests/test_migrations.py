"""Tests for Challenge 095: Database Migration Chain."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from database import InMemoryDB
import migration_001
import migration_002
import migration_003
import migration_004
from migrate import run_migrations


def test_migration_001_creates_users_table():
    db = InMemoryDB()
    migration_001.run(db)
    assert "users" in db.list_tables()
    schema = db.get_schema("users")
    assert "id" in schema
    assert "name" in schema


def test_migration_002_adds_email_column():
    db = InMemoryDB()
    migration_001.run(db)
    migration_002.run(db)
    schema = db.get_schema("users")
    assert "email" in schema


def test_migration_003_creates_orders_table():
    db = InMemoryDB()
    migration_001.run(db)
    migration_002.run(db)
    migration_003.run(db)
    assert "orders" in db.list_tables()
    schema = db.get_schema("orders")
    assert "id" in schema
    assert "user_id" in schema
    assert "total" in schema


def test_migration_004_adds_status_column():
    db = InMemoryDB()
    migration_001.run(db)
    migration_002.run(db)
    migration_003.run(db)
    migration_004.run(db)
    schema = db.get_schema("orders")
    assert "status" in schema


def test_migration_004_status_default_pending():
    db = InMemoryDB()
    migration_001.run(db)
    migration_002.run(db)
    migration_003.run(db)
    db.insert("orders", {"id": 1, "user_id": 1, "total": 99.99})
    migration_004.run(db)
    rows = db.query("orders")
    assert len(rows) == 1
    assert rows[0]["status"] == "pending"


def test_run_migrations_executes_all():
    db = InMemoryDB()
    result = run_migrations(db)
    assert "users" in db.list_tables()
    assert "orders" in db.list_tables()
    users_schema = db.get_schema("users")
    assert "id" in users_schema
    assert "name" in users_schema
    assert "email" in users_schema
    orders_schema = db.get_schema("orders")
    assert "id" in orders_schema
    assert "user_id" in orders_schema
    assert "total" in orders_schema
    assert "status" in orders_schema


def test_insert_user_after_all_migrations():
    db = InMemoryDB()
    run_migrations(db)
    db.insert("users", {"id": 1, "name": "Alice", "email": "alice@example.com"})
    rows = db.query("users")
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"
    assert rows[0]["email"] == "alice@example.com"


def test_insert_order_after_all_migrations():
    db = InMemoryDB()
    run_migrations(db)
    db.insert("users", {"id": 1, "name": "Alice", "email": "alice@example.com"})
    db.insert("orders", {"id": 1, "user_id": 1, "total": 49.99})
    rows = db.query("orders")
    assert len(rows) == 1
    assert rows[0]["user_id"] == 1
    assert rows[0]["total"] == 49.99
    assert rows[0]["status"] is None or rows[0]["status"] == "pending"


def test_query_with_filter():
    db = InMemoryDB()
    run_migrations(db)
    db.insert("users", {"id": 1, "name": "Alice", "email": "alice@example.com"})
    db.insert("users", {"id": 2, "name": "Bob", "email": "bob@example.com"})
    results = db.query("users", lambda r: r["name"] == "Bob")
    assert len(results) == 1
    assert results[0]["name"] == "Bob"


def test_run_migrations_returns_db():
    db = InMemoryDB()
    result = run_migrations(db)
    assert result is db or result is None or isinstance(result, InMemoryDB)
    assert "users" in db.list_tables()
