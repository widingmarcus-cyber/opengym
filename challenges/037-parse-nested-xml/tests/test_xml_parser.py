"""Tests for Challenge 037: Parse Nested XML."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from xml_parser import parse_config

CONFIG_FILE = str(Path(__file__).parent.parent / "setup" / "config.xml")


def test_returns_dict():
    result = parse_config(CONFIG_FILE)
    assert isinstance(result, dict)


def test_total_keys():
    result = parse_config(CONFIG_FILE)
    assert len(result) == 28


def test_simple_nested_values():
    result = parse_config(CONFIG_FILE)
    assert result["database.host"] == "localhost"
    assert result["database.port"] == "5432"
    assert result["cache.provider"] == "redis"


def test_deep_nesting():
    result = parse_config(CONFIG_FILE)
    assert result["database.credentials.username"] == "admin"
    assert result["database.credentials.password"] == "secret123"
    assert result["database.connection.retry.max_attempts"] == "3"
    assert result["database.connection.retry.delay_ms"] == "500"


def test_attributes():
    result = parse_config(CONFIG_FILE)
    assert result["database.connection.@pool_size"] == "10"
    assert result["database.connection.@timeout"] == "30"
    assert result["server.@port"] == "8080"
    assert result["server.@workers"] == "4"


def test_attribute_on_leaf_element():
    result = parse_config(CONFIG_FILE)
    assert result["server.ssl.@enabled"] == "true"
    assert result["server.logging.output.rotation.@max_size"] == "100MB"
    assert result["server.logging.output.rotation.@keep"] == "5"


def test_four_level_nesting():
    result = parse_config(CONFIG_FILE)
    assert result["server.logging.output.file"] == "/var/log/app.log"


def test_notifications_section():
    result = parse_config(CONFIG_FILE)
    assert result["notifications.email.@enabled"] == "true"
    assert result["notifications.email.smtp_host"] == "mail.internal"
    assert result["notifications.email.smtp_port"] == "587"
    assert result["notifications.email.sender"] == "noreply@app.com"
    assert result["notifications.slack.@enabled"] == "false"
    assert result["notifications.slack.webhook_url"] == "https://hooks.slack.com/services/xxx"
    assert result["notifications.slack.channel"] == "#alerts"
