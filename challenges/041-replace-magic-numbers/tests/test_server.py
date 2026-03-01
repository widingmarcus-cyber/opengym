"""Tests for Challenge 041: Replace Magic Numbers."""

import sys
import inspect
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import server
from server import (
    validate_port,
    create_config,
    allocate_buffer,
    check_connections,
    retry_request,
    get_server_defaults,
)


# --- Tests that named constants exist at module level ---

def test_constants_exist():
    """Module-level named constants must be defined."""
    assert hasattr(server, "MAX_PORT"), "Missing constant: MAX_PORT"
    assert hasattr(server, "DEFAULT_TIMEOUT"), "Missing constant: DEFAULT_TIMEOUT"
    assert hasattr(server, "MAX_RETRIES"), "Missing constant: MAX_RETRIES"
    assert hasattr(server, "BUFFER_SIZE"), "Missing constant: BUFFER_SIZE"
    assert hasattr(server, "DEFAULT_PORT"), "Missing constant: DEFAULT_PORT"
    assert hasattr(server, "MAX_CONNECTIONS"), "Missing constant: MAX_CONNECTIONS"


def test_constant_values():
    """Constants must have the correct values."""
    assert server.MAX_PORT == 65535
    assert server.DEFAULT_TIMEOUT == 30
    assert server.MAX_RETRIES == 3
    assert server.BUFFER_SIZE == 4096
    assert server.DEFAULT_PORT == 8080
    assert server.MAX_CONNECTIONS == 100


# --- Tests that functions still work correctly ---

def test_validate_port_valid():
    assert validate_port(80) == 80
    assert validate_port(8080) == 8080
    assert validate_port(65535) == 65535


def test_validate_port_invalid():
    import pytest
    with pytest.raises(ValueError):
        validate_port(0)
    with pytest.raises(ValueError):
        validate_port(70000)
    with pytest.raises(TypeError):
        validate_port("80")


def test_create_config_defaults():
    config = create_config()
    assert config["host"] == "localhost"
    assert config["port"] == 8080
    assert config["timeout"] == 30
    assert config["retries"] == 3
    assert config["buffer_size"] == 4096
    assert config["max_connections"] == 100


def test_allocate_buffer():
    assert allocate_buffer(1) == 4096
    assert allocate_buffer(4) == 16384


def test_check_connections():
    result = check_connections(50)
    assert result["accept"] is True
    assert result["remaining"] == 50

    full = check_connections(100)
    assert full["accept"] is False
    assert full["remaining"] == 0


def test_retry_request_success():
    success, result = retry_request(lambda: 42)
    assert success is True
    assert result == 42


# --- Tests that constants are actually USED inside function bodies ---

def test_validate_port_uses_max_port_constant():
    """validate_port must reference MAX_PORT, not the literal 65535."""
    source = inspect.getsource(validate_port)
    assert "MAX_PORT" in source, (
        "validate_port should use the MAX_PORT constant instead of a magic number"
    )


def test_validate_port_no_magic_65535():
    """validate_port must not contain the literal number 65535."""
    source = inspect.getsource(validate_port)
    assert "65535" not in source, (
        "validate_port still contains the magic number 65535 — use MAX_PORT instead"
    )


def test_allocate_buffer_uses_buffer_size_constant():
    """allocate_buffer must reference BUFFER_SIZE, not the literal 4096."""
    source = inspect.getsource(allocate_buffer)
    assert "BUFFER_SIZE" in source, (
        "allocate_buffer should use the BUFFER_SIZE constant instead of a magic number"
    )


def test_allocate_buffer_no_magic_4096():
    """allocate_buffer must not contain the literal number 4096."""
    source = inspect.getsource(allocate_buffer)
    assert "4096" not in source, (
        "allocate_buffer still contains the magic number 4096 — use BUFFER_SIZE instead"
    )


def test_check_connections_uses_max_connections_constant():
    """check_connections must reference MAX_CONNECTIONS, not the literal 100."""
    source = inspect.getsource(check_connections)
    assert "MAX_CONNECTIONS" in source, (
        "check_connections should use the MAX_CONNECTIONS constant instead of a magic number"
    )


def test_create_config_uses_constants():
    """create_config must reference named constants, not magic numbers."""
    source = inspect.getsource(create_config)
    assert "DEFAULT_PORT" in source, (
        "create_config should use DEFAULT_PORT instead of the literal 8080"
    )
    assert "DEFAULT_TIMEOUT" in source, (
        "create_config should use DEFAULT_TIMEOUT instead of the literal 30"
    )
    assert "MAX_RETRIES" in source, (
        "create_config should use MAX_RETRIES instead of the literal 3"
    )
    assert "BUFFER_SIZE" in source, (
        "create_config should use BUFFER_SIZE instead of the literal 4096"
    )
    assert "MAX_CONNECTIONS" in source, (
        "create_config should use MAX_CONNECTIONS instead of the literal 100"
    )
