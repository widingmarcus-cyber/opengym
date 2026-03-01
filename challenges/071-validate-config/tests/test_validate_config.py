"""Tests for Challenge 071: Validate Config."""

import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from config_loader import load_config


VALID_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "myapp",
    "data_dir": "/var/data/myapp",
}


def test_valid_config_accepted():
    result = load_config(VALID_CONFIG)
    assert result["host"] == "localhost"
    assert result["port"] == 5432
    assert result["database"] == "myapp"


def test_valid_config_high_port():
    config = {**VALID_CONFIG, "port": 65535}
    result = load_config(config)
    assert result["port"] == 65535


def test_reject_negative_port():
    config = {**VALID_CONFIG, "port": -1}
    with pytest.raises(ValueError):
        load_config(config)


def test_reject_zero_port():
    config = {**VALID_CONFIG, "port": 0}
    with pytest.raises(ValueError):
        load_config(config)


def test_reject_port_above_max():
    config = {**VALID_CONFIG, "port": 70000}
    with pytest.raises(ValueError):
        load_config(config)


def test_reject_path_traversal():
    config = {**VALID_CONFIG, "data_dir": "../../etc/passwd"}
    with pytest.raises(ValueError):
        load_config(config)


def test_reject_path_traversal_middle():
    config = {**VALID_CONFIG, "data_dir": "/var/data/../../../etc/shadow"}
    with pytest.raises(ValueError):
        load_config(config)


def test_reject_empty_database_name():
    config = {**VALID_CONFIG, "database": ""}
    with pytest.raises(ValueError):
        load_config(config)


def test_reject_whitespace_database_name():
    config = {**VALID_CONFIG, "database": "   "}
    with pytest.raises(ValueError):
        load_config(config)


def test_reject_empty_host():
    config = {**VALID_CONFIG, "host": ""}
    with pytest.raises(ValueError):
        load_config(config)
