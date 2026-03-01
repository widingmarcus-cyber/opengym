"""Tests for Challenge 044: Decompose the God Class."""

import sys
import inspect
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import app_manager
from app_manager import AppManager


# --- Tests that the four decomposed classes exist ---

def test_database_manager_class_exists():
    assert hasattr(app_manager, "DatabaseManager"), "DatabaseManager class must exist"
    db = app_manager.DatabaseManager()
    for method in ("connect", "disconnect", "query", "insert", "update", "delete"):
        assert hasattr(db, method), f"DatabaseManager must have method: {method}"


def test_cache_manager_class_exists():
    assert hasattr(app_manager, "CacheManager"), "CacheManager class must exist"
    cache = app_manager.CacheManager()
    for method in ("get_cache", "set_cache", "clear_cache", "get_cache_stats"):
        assert hasattr(cache, method), f"CacheManager must have method: {method}"


def test_validator_class_exists():
    assert hasattr(app_manager, "Validator"), "Validator class must exist"
    v = app_manager.Validator()
    for method in ("validate_user", "validate_order", "validate_email", "validate_phone", "validate_address"):
        assert hasattr(v, method), f"Validator must have method: {method}"


def test_formatter_class_exists():
    assert hasattr(app_manager, "Formatter"), "Formatter class must exist"
    f = app_manager.Formatter()
    for method in ("format_report", "format_email", "format_csv", "format_json_response", "format_log_entry"):
        assert hasattr(f, method), f"Formatter must have method: {method}"


# --- Tests that component classes work independently ---

def test_database_manager_independent():
    db = app_manager.DatabaseManager()
    result = db.connect("test_db")
    assert result["status"] == "connected"
    db.insert("users", {"name": "Alice"})
    records = db.query("users")
    assert len(records) == 1
    assert records[0]["name"] == "Alice"
    db.disconnect()


def test_cache_manager_independent():
    cache = app_manager.CacheManager()
    cache.set_cache("key1", "value1", ttl=3600)
    assert cache.get_cache("key1") == "value1"
    assert cache.get_cache("missing") is None
    stats = cache.get_cache_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1


def test_validator_independent():
    v = app_manager.Validator()
    assert v.validate_email("test@example.com") is True
    assert v.validate_email("invalid") is False
    assert v.validate_phone("+1 (555) 123-4567") is True
    result = v.validate_address({"street": "123 Main", "city": "NY", "state": "NY", "zip_code": "10001"})
    assert result["valid"] is True


def test_formatter_independent():
    f = app_manager.Formatter()
    csv = f.format_csv(["name", "age"], [["Alice", 30], ["Bob", 25]])
    assert "name,age" in csv
    assert "Alice,30" in csv
    email = f.format_email("a@b.com", "Hello", "World")
    assert email["to"] == "a@b.com"
    assert "Subject: Hello" in email["formatted"]


# --- Tests that AppManager uses composition and still works as facade ---

def test_app_manager_has_component_attributes():
    mgr = AppManager()
    assert hasattr(mgr, "db"), "AppManager must have a 'db' attribute"
    assert hasattr(mgr, "cache"), "AppManager must have a 'cache' attribute"
    assert hasattr(mgr, "validator"), "AppManager must have a 'validator' attribute"
    assert hasattr(mgr, "formatter"), "AppManager must have a 'formatter' attribute"


def test_app_manager_database_facade():
    mgr = AppManager()
    mgr.connect("mydb")
    mgr.insert("products", {"name": "Widget", "price": 9.99})
    mgr.insert("products", {"name": "Gadget", "price": 19.99})
    results = mgr.query("products", {"name": "Widget"})
    assert len(results) == 1
    assert results[0]["price"] == 9.99
    mgr.update("products", 2, {"price": 24.99})
    updated = mgr.query("products", {"name": "Gadget"})
    assert updated[0]["price"] == 24.99
    mgr.delete("products", 1)
    remaining = mgr.query("products")
    assert len(remaining) == 1
    mgr.disconnect()


def test_app_manager_full_workflow():
    mgr = AppManager()
    mgr.connect("app_db")

    user_data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    validation = mgr.validate_user(user_data)
    assert validation["valid"] is True

    mgr.insert("users", user_data)
    mgr.set_cache("user:alice", user_data)
    cached = mgr.get_cache("user:alice")
    assert cached["name"] == "Alice"

    users = mgr.query("users")
    report = mgr.format_report("User Report", users)
    assert "USER REPORT" in report
    assert "Alice" in report

    stats = mgr.get_cache_stats()
    assert stats["hits"] >= 1

    mgr.clear_cache()
    mgr.disconnect()


def test_app_manager_validation_and_formatting_facade():
    mgr = AppManager()
    order_valid = mgr.validate_order({"product": "Widget", "quantity": 2, "price": 9.99})
    assert order_valid["valid"] is True

    order_invalid = mgr.validate_order({"product": "", "quantity": 0, "price": -1})
    assert order_invalid["valid"] is False
    assert len(order_invalid["errors"]) >= 2

    log = mgr.format_log_entry("error", "something went wrong")
    assert "[ERROR]" in log
    assert "something went wrong" in log

    resp = mgr.format_json_response({"id": 1}, status="success")
    assert resp["status"] == "success"
    assert resp["data"]["id"] == 1
