"""Tests for Challenge 056: Search the Codebase."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from answers import (
    how_many_functions,
    what_is_the_entry_point,
    list_all_imports,
    which_file_has_most_lines,
    list_all_classes,
    what_database_engine,
    how_many_routes,
    find_todo_comments,
)


def test_how_many_functions():
    assert how_many_functions() == 24


def test_what_is_the_entry_point():
    assert what_is_the_entry_point() == "app.py"


def test_list_all_imports():
    result = list_all_imports()
    expected = [
        "config",
        "database",
        "datetime",
        "hashlib",
        "json",
        "models",
        "os",
        "re",
        "routes",
        "sqlite3",
        "utils",
    ]
    assert result == expected


def test_which_file_has_most_lines():
    assert which_file_has_most_lines() == "models.py"


def test_list_all_classes():
    result = list_all_classes()
    expected = ["Comment", "DatabaseConnection", "Post", "User"]
    assert result == expected


def test_what_database_engine():
    assert what_database_engine() == "postgresql"


def test_how_many_routes():
    assert how_many_routes() == 5


def test_find_todo_comments():
    result = find_todo_comments()
    expected = [
        "add connection pooling support",
        "add input sanitization function",
        "add production configuration class",
        "add rate limiting helper",
    ]
    assert result == expected
