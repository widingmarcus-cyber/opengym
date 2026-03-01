"""Tests for Challenge 054: OAuth Token Flow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from auth_server import AuthServer
from oauth_client import OAuthClient


def make_clock(start=0.0):
    current = [start]

    def tick():
        return current[0]

    def advance(seconds):
        current[0] += seconds

    return tick, advance


def make_server(ttl=3600):
    return AuthServer(valid_clients={"app": "secret123"}, token_ttl=ttl)


def test_authenticate_success():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    client.authenticate()
    assert client.is_authenticated() is True


def test_authenticate_invalid_credentials():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "wrong", time_fn=clock)
    with pytest.raises(ValueError):
        client.authenticate()


def test_get_token_auto_authenticates():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    token = client.get_token()
    assert isinstance(token, str)
    assert len(token) > 0


def test_get_token_returns_cached():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    token1 = client.get_token()
    token2 = client.get_token()
    assert token1 == token2


def test_get_token_refreshes_after_expiry():
    server = make_server(ttl=10)
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    token1 = client.get_token()
    advance(11)
    token2 = client.get_token()
    assert token1 != token2


def test_is_authenticated_false_initially():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    assert client.is_authenticated() is False


def test_is_authenticated_false_after_expiry():
    server = make_server(ttl=5)
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    client.authenticate()
    assert client.is_authenticated() is True
    advance(6)
    assert client.is_authenticated() is False


def test_revoke_clears_token():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    token = client.get_token()
    assert server.validate(token) is True
    client.revoke()
    assert client.is_authenticated() is False
    assert server.validate(token) is False


def test_revoke_when_not_authenticated():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    client.revoke()
    assert client.is_authenticated() is False


def test_get_token_after_revoke():
    server = make_server()
    clock, advance = make_clock()
    client = OAuthClient(server, "app", "secret123", time_fn=clock)
    token1 = client.get_token()
    client.revoke()
    token2 = client.get_token()
    assert token1 != token2
    assert client.is_authenticated() is True
