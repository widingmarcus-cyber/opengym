"""Tests for Challenge 092: Merge Config Files."""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from config_merger import merge_configs

SETUP_DIR = str(Path(__file__).parent.parent / "setup")


def _write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def test_single_json_file():
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "a.json")
        _write_json(p, {"x": 1, "y": 2})
        result = merge_configs([p])
        assert result == {"x": 1, "y": 2}


def test_deep_merge_nested_dicts():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.json")
        p2 = os.path.join(tmp, "b.json")
        _write_json(p1, {"db": {"host": "localhost", "port": 5432}})
        _write_json(p2, {"db": {"port": 5433, "name": "mydb"}})
        result = merge_configs([p1, p2])
        assert result["db"]["host"] == "localhost"
        assert result["db"]["port"] == 5433
        assert result["db"]["name"] == "mydb"


def test_lists_are_replaced():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.json")
        p2 = os.path.join(tmp, "b.json")
        _write_json(p1, {"tags": ["a", "b"]})
        _write_json(p2, {"tags": ["c"]})
        result = merge_configs([p1, p2])
        assert result["tags"] == ["c"]


def test_last_wins_precedence():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.json")
        p2 = os.path.join(tmp, "b.json")
        _write_json(p1, {"debug": False, "level": 1})
        _write_json(p2, {"debug": True, "level": 2})
        result = merge_configs([p1, p2], precedence="last_wins")
        assert result["debug"] is True
        assert result["level"] == 2


def test_first_wins_precedence():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.json")
        p2 = os.path.join(tmp, "b.json")
        _write_json(p1, {"debug": False, "level": 1})
        _write_json(p2, {"debug": True, "level": 2})
        result = merge_configs([p1, p2], precedence="first_wins")
        assert result["debug"] is False
        assert result["level"] == 1


def test_merge_json_and_yaml():
    base_json = os.path.join(SETUP_DIR, "base.json")
    override_yaml = os.path.join(SETUP_DIR, "override.yaml")
    result = merge_configs([base_json, override_yaml])
    assert result["database"]["port"] == 5433
    assert result["database"]["host"] == "localhost"
    assert result["debug"] is True
    assert result["log_level"] == "info"


def test_merge_all_three_formats():
    base_json = os.path.join(SETUP_DIR, "base.json")
    override_yaml = os.path.join(SETUP_DIR, "override.yaml")
    local_toml = os.path.join(SETUP_DIR, "local.toml")
    result = merge_configs([base_json, override_yaml, local_toml])
    assert result["database"]["host"] == "127.0.0.1"
    assert result["database"]["port"] == 5434
    assert result["database"]["options"]["timeout"] == 60
    assert result["database"]["options"]["ssl"] is True
    assert result["debug"] is False
    assert result["log_level"] == "debug"


def test_deep_merge_preserves_unrelated_keys():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.json")
        p2 = os.path.join(tmp, "b.json")
        _write_json(p1, {"a": {"x": 1, "y": 2}, "b": 10})
        _write_json(p2, {"a": {"z": 3}, "c": 20})
        result = merge_configs([p1, p2])
        assert result["a"] == {"x": 1, "y": 2, "z": 3}
        assert result["b"] == 10
        assert result["c"] == 20
