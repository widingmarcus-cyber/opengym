"""Tests for Challenge 053: API Response Caching."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from api import FakeAPI
from cached_client import CachedClient


def make_clock(start=0.0):
    current = [start]

    def tick():
        return current[0]

    def advance(seconds):
        current[0] += seconds

    return tick, advance


def test_get_calls_api_on_miss():
    api = FakeAPI({"user": "Alice"})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=10, time_fn=clock)
    result = client.get("user")
    assert result == "Alice"
    assert api.call_count == 1


def test_get_returns_cached_on_hit():
    api = FakeAPI({"user": "Alice"})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=10, time_fn=clock)
    client.get("user")
    client.get("user")
    assert api.call_count == 1


def test_get_refetches_after_ttl_expires():
    api = FakeAPI({"user": "Alice"})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=5, time_fn=clock)
    client.get("user")
    assert api.call_count == 1
    advance(6)
    client.get("user")
    assert api.call_count == 2


def test_invalidate_removes_cached_key():
    api = FakeAPI({"user": "Alice"})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=60, time_fn=clock)
    client.get("user")
    client.invalidate("user")
    client.get("user")
    assert api.call_count == 2


def test_clear_removes_all_cached():
    api = FakeAPI({"a": 1, "b": 2})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=60, time_fn=clock)
    client.get("a")
    client.get("b")
    assert api.call_count == 2
    client.clear()
    client.get("a")
    client.get("b")
    assert api.call_count == 4


def test_stats_tracks_hits_and_misses():
    api = FakeAPI({"x": 42})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=60, time_fn=clock)
    client.get("x")
    client.get("x")
    client.get("x")
    stats = client.stats()
    assert stats == {"hits": 2, "misses": 1}


def test_stats_after_expiry():
    api = FakeAPI({"x": 42})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=5, time_fn=clock)
    client.get("x")
    advance(10)
    client.get("x")
    stats = client.stats()
    assert stats == {"hits": 0, "misses": 2}


def test_multiple_keys_independent_ttl():
    api = FakeAPI({"a": 1, "b": 2})
    clock, advance = make_clock()
    client = CachedClient(api, ttl=10, time_fn=clock)
    client.get("a")
    advance(5)
    client.get("b")
    advance(6)
    client.get("a")
    client.get("b")
    assert api.call_count == 3
    stats = client.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 3
