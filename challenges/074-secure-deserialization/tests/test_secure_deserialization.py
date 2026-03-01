"""Tests for Challenge 074: Secure Deserialization."""

import sys
import os
import pickle
import pytest
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from storage import save, load


@pytest.fixture
def tmp_file(tmp_path):
    return str(tmp_path / "data.json")


@pytest.fixture
def pickle_file(tmp_path):
    filepath = str(tmp_path / "malicious.pkl")
    with open(filepath, "wb") as f:
        pickle.dump({"key": "value"}, f)
    return filepath


def test_roundtrip_basic_types(tmp_file):
    data = {"name": "Alice", "age": 30, "score": 95.5, "active": True, "extra": None}
    save(data, tmp_file)
    result = load(tmp_file)
    assert result == data


def test_roundtrip_list(tmp_file):
    data = [1, 2, 3, "hello", True, None]
    save(data, tmp_file)
    result = load(tmp_file)
    assert result == data


def test_roundtrip_nested(tmp_file):
    data = {"users": [{"name": "Bob", "scores": [10, 20, 30]}]}
    save(data, tmp_file)
    result = load(tmp_file)
    assert result == data


def test_roundtrip_datetime(tmp_file):
    dt = datetime(2024, 6, 15, 10, 30, 0)
    data = {"timestamp": dt}
    save(data, tmp_file)
    result = load(tmp_file)
    assert isinstance(result["timestamp"], datetime)
    assert result["timestamp"] == dt


def test_roundtrip_set(tmp_file):
    data = {"tags": {1, 2, 3}}
    save(data, tmp_file)
    result = load(tmp_file)
    assert isinstance(result["tags"], set)
    assert result["tags"] == {1, 2, 3}


def test_roundtrip_bytes(tmp_file):
    data = {"payload": b"hello world"}
    save(data, tmp_file)
    result = load(tmp_file)
    assert isinstance(result["payload"], bytes)
    assert result["payload"] == b"hello world"


def test_custom_object_saved_as_dict(tmp_file):
    class User:
        def __init__(self, name, email):
            self.name = name
            self.email = email

    user = User("Alice", "alice@example.com")
    data = {"user": user}
    save(data, tmp_file)
    result = load(tmp_file)
    assert isinstance(result["user"], dict)
    assert result["user"]["name"] == "Alice"
    assert result["user"]["email"] == "alice@example.com"


def test_no_pickle_used(tmp_file):
    data = {"key": "value"}
    save(data, tmp_file)
    with open(tmp_file, "rb") as f:
        first_bytes = f.read(2)
    assert first_bytes != b"\x80\x04", "File should not be pickle format"
    assert first_bytes != b"\x80\x05", "File should not be pickle format"
    content = Path(tmp_file).read_text(encoding="utf-8")
    assert "key" in content, "File should be human-readable (JSON)"


def test_reject_pickle_file(pickle_file):
    with pytest.raises((ValueError, Exception)):
        load(pickle_file)


def test_file_is_json_readable(tmp_file):
    import json
    data = {"message": "hello", "count": 42}
    save(data, tmp_file)
    with open(tmp_file, "r") as f:
        parsed = json.load(f)
    assert isinstance(parsed, dict)


def test_saved_file_is_valid_json_with_list(tmp_file):
    """Saved file must be parseable as JSON even for list data."""
    import json
    data = [1, 2, 3, "test"]
    save(data, tmp_file)
    with open(tmp_file, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert parsed == data, f"JSON content mismatch: {parsed} != {data}"


def test_no_pickle_magic_bytes_any_protocol(tmp_file):
    """File must not start with pickle magic byte 0x80 (any protocol version)."""
    data = {"secure": True, "value": 123}
    save(data, tmp_file)
    with open(tmp_file, "rb") as f:
        first_byte = f.read(1)
    assert first_byte != b"\x80", \
        f"File starts with pickle magic byte 0x80 — data is pickled, not JSON"


def test_custom_object_serialized_to_dict_not_pickle(tmp_file):
    """Custom objects should be serialized as plain dicts, verifiable via JSON parsing."""
    import json

    class Config:
        def __init__(self, host, port):
            self.host = host
            self.port = port

    obj = Config("localhost", 8080)
    save({"config": obj}, tmp_file)
    with open(tmp_file, "r", encoding="utf-8") as f:
        parsed = json.load(f)
    assert isinstance(parsed["config"], dict)
    assert parsed["config"]["host"] == "localhost"
    assert parsed["config"]["port"] == 8080
