"""Tests for Challenge 023: Create Retry Decorator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from retry import retry


def test_succeeds_first_try():
    sleep_calls = []

    @retry(sleep_func=lambda d: sleep_calls.append(d))
    def always_works():
        return 42

    assert always_works() == 42
    assert sleep_calls == []


def test_succeeds_after_retries():
    attempts = [0]
    sleep_calls = []

    @retry(max_attempts=3, delay=1.0, backoff=2.0, sleep_func=lambda d: sleep_calls.append(d))
    def fail_twice():
        attempts[0] += 1
        if attempts[0] < 3:
            raise ValueError("not yet")
        return "done"

    assert fail_twice() == "done"
    assert attempts[0] == 3
    assert sleep_calls == [1.0, 2.0]


def test_exhausts_attempts():
    sleep_calls = []

    @retry(max_attempts=3, delay=0.5, backoff=2.0, sleep_func=lambda d: sleep_calls.append(d))
    def always_fails():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError, match="fail"):
        always_fails()
    assert len(sleep_calls) == 2


def test_exponential_backoff_delays():
    sleep_calls = []

    @retry(max_attempts=4, delay=1.0, backoff=3.0, sleep_func=lambda d: sleep_calls.append(d))
    def always_fails():
        raise ValueError("fail")

    with pytest.raises(ValueError):
        always_fails()
    assert sleep_calls == [1.0, 3.0, 9.0]


def test_only_catches_specified_exceptions():
    sleep_calls = []

    @retry(max_attempts=3, exceptions=(ValueError,), sleep_func=lambda d: sleep_calls.append(d))
    def raises_type_error():
        raise TypeError("wrong type")

    with pytest.raises(TypeError):
        raises_type_error()
    assert sleep_calls == []


def test_catches_multiple_exception_types():
    attempts = [0]
    sleep_calls = []

    @retry(max_attempts=3, exceptions=(ValueError, KeyError), sleep_func=lambda d: sleep_calls.append(d))
    def alternating_errors():
        attempts[0] += 1
        if attempts[0] == 1:
            raise ValueError("val")
        if attempts[0] == 2:
            raise KeyError("key")
        return "ok"

    assert alternating_errors() == "ok"
    assert attempts[0] == 3


def test_default_max_attempts():
    attempts = [0]
    sleep_calls = []

    @retry(sleep_func=lambda d: sleep_calls.append(d))
    def always_fails():
        attempts[0] += 1
        raise Exception("fail")

    with pytest.raises(Exception):
        always_fails()
    assert attempts[0] == 3


def test_single_attempt():
    sleep_calls = []

    @retry(max_attempts=1, sleep_func=lambda d: sleep_calls.append(d))
    def always_fails():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        always_fails()
    assert sleep_calls == []
