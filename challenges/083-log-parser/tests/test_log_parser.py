"""Tests for Challenge 083: Log Parser."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from log_parser import parse_line, parse_file, count_by_level, errors_per_hour

LOG_FILE = str(Path(__file__).parent.parent / "setup" / "access.log")


def test_parse_line_returns_dict():
    line = "2024-01-15 10:30:00 [INFO] UserService: User logged in (user_id=42)"
    result = parse_line(line)
    assert isinstance(result, dict)
    assert set(result.keys()) == {"timestamp", "level", "service", "message"}


def test_parse_line_extracts_fields():
    line = "2024-01-15 08:10:00 [ERROR] PaymentService: Failed to connect to payment gateway"
    result = parse_line(line)
    assert result["timestamp"] == "2024-01-15 08:10:00"
    assert result["level"] == "ERROR"
    assert result["service"] == "PaymentService"
    assert result["message"] == "Failed to connect to payment gateway"


def test_parse_line_debug_level():
    line = "2024-01-15 08:02:00 [DEBUG] ConfigLoader: Loading configuration from /etc/app/config.yaml"
    result = parse_line(line)
    assert result["level"] == "DEBUG"
    assert result["service"] == "ConfigLoader"
    assert result["message"] == "Loading configuration from /etc/app/config.yaml"


def test_parse_file_returns_list():
    entries = parse_file(LOG_FILE)
    assert isinstance(entries, list)
    assert len(entries) == 116
    assert all(isinstance(e, dict) for e in entries)


def test_parse_file_first_entry():
    entries = parse_file(LOG_FILE)
    assert entries[0]["timestamp"] == "2024-01-15 08:00:00"
    assert entries[0]["level"] == "INFO"
    assert entries[0]["service"] == "AppServer"
    assert entries[0]["message"] == "Application started successfully"


def test_count_by_level_values():
    entries = parse_file(LOG_FILE)
    counts = count_by_level(entries)
    assert isinstance(counts, dict)
    assert counts["INFO"] == 67
    assert counts["WARN"] == 15
    assert counts["ERROR"] == 11
    assert counts["DEBUG"] == 23


def test_count_by_level_total():
    entries = parse_file(LOG_FILE)
    counts = count_by_level(entries)
    assert sum(counts.values()) == 116


def test_errors_per_hour():
    entries = parse_file(LOG_FILE)
    result = errors_per_hour(entries)
    assert isinstance(result, dict)
    assert result[8] == 2
    assert result[9] == 2
    assert result[10] == 3
    assert result[11] == 2
    assert result[12] == 1
    assert result[13] == 1
