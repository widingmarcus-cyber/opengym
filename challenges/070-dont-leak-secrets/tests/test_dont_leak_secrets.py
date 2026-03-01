"""Tests for Challenge 070: Don't Leak Secrets."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from logger import log_request

REDACTED = "***REDACTED***"


def test_normal_request_logged():
    result = log_request(
        "GET", "https://example.com/health",
        {"Accept": "application/json"}, {}
    )
    assert "GET" in result
    assert "https://example.com/health" in result
    assert "Accept" in result


def test_method_preserved():
    result = log_request("POST", "https://example.com/data",
                         {"Content-Type": "text/plain"}, {"key": "value"})
    assert "POST" in result


def test_authorization_header_redacted():
    result = log_request(
        "GET", "https://example.com/api",
        {"Authorization": "Bearer secret_token_123", "Accept": "text/html"},
        {}
    )
    assert "secret_token_123" not in result
    assert REDACTED in result


def test_api_key_in_url_redacted():
    result = log_request(
        "GET", "https://api.example.com/data?api_key=sk_live_abc123&page=1",
        {"Accept": "application/json"}, {}
    )
    assert "sk_live_abc123" not in result
    assert REDACTED in result


def test_password_in_body_redacted():
    result = log_request(
        "POST", "https://example.com/login",
        {"Content-Type": "application/json"},
        {"username": "admin", "password": "supersecret123"}
    )
    assert "supersecret123" not in result
    assert REDACTED in result
    assert "admin" in result


def test_safe_headers_not_redacted():
    result = log_request(
        "GET", "https://example.com/api",
        {"Content-Type": "application/json", "Accept": "text/html"},
        {}
    )
    assert "application/json" in result
    assert "text/html" in result


def test_safe_body_fields_not_redacted():
    result = log_request(
        "POST", "https://example.com/data",
        {},
        {"name": "Alice", "email": "alice@example.com"}
    )
    assert "Alice" in result
    assert "alice@example.com" in result


def test_multiple_secrets_all_redacted():
    result = log_request(
        "POST",
        "https://api.example.com/users?api_key=my_secret_key",
        {"Authorization": "Basic dXNlcjpwYXNz"},
        {"password": "hunter2", "username": "admin"}
    )
    assert "my_secret_key" not in result
    assert "dXNlcjpwYXNz" not in result
    assert "hunter2" not in result
    assert result.count(REDACTED) >= 3


def test_token_in_body_redacted():
    """Secret 'token' field in body must be redacted."""
    result = log_request(
        "POST", "https://example.com/webhook",
        {"Content-Type": "application/json"},
        {"token": "ghp_abc123secret456", "event": "push"}
    )
    assert "ghp_abc123secret456" not in result
    assert REDACTED in result
    assert "push" in result


def test_x_api_key_header_redacted():
    """X-API-Key header must be redacted."""
    result = log_request(
        "GET", "https://example.com/data",
        {"X-API-Key": "key_prod_9876", "Accept": "application/json"},
        {}
    )
    assert "key_prod_9876" not in result
    assert REDACTED in result
    assert "application/json" in result


def test_secret_in_body_redacted():
    """Secret 'secret' field in body must be redacted."""
    result = log_request(
        "POST", "https://example.com/config",
        {},
        {"secret": "s3cr3t_v4lue", "name": "my-app"}
    )
    assert "s3cr3t_v4lue" not in result
    assert REDACTED in result
    assert "my-app" in result


def test_cookie_header_redacted():
    """Cookie header must be redacted as it may contain session secrets."""
    result = log_request(
        "GET", "https://example.com/profile",
        {"Cookie": "session=abc123xyz789", "Accept": "text/html"},
        {}
    )
    assert "abc123xyz789" not in result
    assert REDACTED in result
    assert "text/html" in result
