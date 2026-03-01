"""Tests for Challenge 021: Implement Rate Limiter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from rate_limiter import RateLimiter


def make_clock(start=0.0):
    current = [start]

    def tick():
        return current[0]

    def advance(seconds):
        current[0] += seconds

    return tick, advance


def test_allow_within_limit():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("api", max_tokens=3, refill_rate=1.0)
    assert limiter.allow("api") is True
    assert limiter.allow("api") is True
    assert limiter.allow("api") is True


def test_deny_when_exhausted():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("api", max_tokens=2, refill_rate=1.0)
    assert limiter.allow("api") is True
    assert limiter.allow("api") is True
    assert limiter.allow("api") is False


def test_refill_over_time():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("api", max_tokens=2, refill_rate=1.0)
    assert limiter.allow("api") is True
    assert limiter.allow("api") is True
    assert limiter.allow("api") is False
    advance(1.0)
    assert limiter.allow("api") is True


def test_refill_does_not_exceed_max():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("api", max_tokens=3, refill_rate=10.0)
    assert limiter.allow("api") is True
    advance(100.0)
    assert limiter.allow("api") is True
    assert limiter.allow("api") is True
    assert limiter.allow("api") is True
    assert limiter.allow("api") is False


def test_per_key_isolation():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("fast", max_tokens=1, refill_rate=1.0)
    limiter.configure("slow", max_tokens=5, refill_rate=1.0)
    assert limiter.allow("fast") is True
    assert limiter.allow("fast") is False
    assert limiter.allow("slow") is True
    assert limiter.allow("slow") is True


def test_reset():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("api", max_tokens=2, refill_rate=1.0)
    limiter.allow("api")
    limiter.allow("api")
    assert limiter.allow("api") is False
    limiter.reset("api")
    assert limiter.allow("api") is True
    assert limiter.allow("api") is True


def test_allow_unconfigured_key_raises():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    with pytest.raises(ValueError):
        limiter.allow("unknown")


def test_reset_unconfigured_key_raises():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    with pytest.raises(ValueError):
        limiter.reset("unknown")


def test_partial_refill():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("api", max_tokens=5, refill_rate=2.0)
    for _ in range(5):
        limiter.allow("api")
    assert limiter.allow("api") is False
    advance(0.5)
    assert limiter.allow("api") is True
    assert limiter.allow("api") is False


def test_burst_then_steady():
    clock, advance = make_clock()
    limiter = RateLimiter(time_func=clock)
    limiter.configure("api", max_tokens=5, refill_rate=1.0)
    for _ in range(5):
        assert limiter.allow("api") is True
    assert limiter.allow("api") is False
    for i in range(3):
        advance(1.0)
        assert limiter.allow("api") is True
