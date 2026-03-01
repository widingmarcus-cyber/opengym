"""Tests for Challenge 072: Rate Limit Endpoint."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from handler import handle_request


def make_time_fn(start=1000.0):
    current = [start]

    def time_fn():
        return current[0]

    def advance(seconds):
        current[0] += seconds

    return time_fn, advance


def test_single_request_succeeds():
    time_fn, _ = make_time_fn()
    result = handle_request("client1", {"action": "ping"}, time_fn=time_fn)
    assert result["status"] == "ok"


def test_ten_requests_all_succeed():
    time_fn, _ = make_time_fn()
    for i in range(10):
        result = handle_request("client_a", {"action": f"req{i}"}, time_fn=time_fn)
        assert result["status"] == "ok", f"Request {i+1} should succeed"


def test_eleventh_request_rejected():
    time_fn, _ = make_time_fn()
    for i in range(10):
        handle_request("client_b", {"action": f"req{i}"}, time_fn=time_fn)
    result = handle_request("client_b", {"action": "req10"}, time_fn=time_fn)
    assert result["status"] == "error"
    assert "rate limit" in result.get("message", "").lower() or \
           "exceeded" in result.get("message", "").lower()


def test_different_clients_independent():
    time_fn, _ = make_time_fn()
    for i in range(10):
        handle_request("client_x", {"action": f"req{i}"}, time_fn=time_fn)

    result = handle_request("client_y", {"action": "req0"}, time_fn=time_fn)
    assert result["status"] == "ok", "Different client should not be rate limited"


def test_rate_limit_resets_after_window():
    time_fn, advance = make_time_fn()
    for i in range(10):
        handle_request("client_c", {"action": f"req{i}"}, time_fn=time_fn)

    result = handle_request("client_c", {"action": "blocked"}, time_fn=time_fn)
    assert result["status"] == "error"

    advance(61)
    result = handle_request("client_c", {"action": "allowed"}, time_fn=time_fn)
    assert result["status"] == "ok", "Should allow requests after window resets"


def test_response_contains_data():
    time_fn, _ = make_time_fn()
    result = handle_request("client_d", {"action": "test"}, time_fn=time_fn)
    assert result["status"] == "ok"
    assert "data" in result


def test_error_response_has_message():
    time_fn, _ = make_time_fn()
    for i in range(10):
        handle_request("client_e", {"action": f"req{i}"}, time_fn=time_fn)
    result = handle_request("client_e", {"action": "overflow"}, time_fn=time_fn)
    assert result["status"] == "error"
    assert "message" in result


def test_partial_window_reset():
    time_fn, advance = make_time_fn()
    for i in range(5):
        handle_request("client_f", {"action": f"req{i}"}, time_fn=time_fn)

    advance(30)
    for i in range(5):
        handle_request("client_f", {"action": f"req{i+5}"}, time_fn=time_fn)

    result = handle_request("client_f", {"action": "over"}, time_fn=time_fn)
    assert result["status"] == "error"


def test_rate_limited_response_status_code():
    """Rate-limited response should include a 429 status code or equivalent."""
    time_fn, _ = make_time_fn()
    for i in range(10):
        handle_request("client_g", {"action": f"req{i}"}, time_fn=time_fn)
    result = handle_request("client_g", {"action": "over"}, time_fn=time_fn)
    assert result["status"] == "error"
    # Response must include either a status_code field or a message indicating rate limiting
    has_status_code = result.get("status_code") == 429
    has_rate_limit_msg = "rate" in result.get("message", "").lower()
    assert has_status_code or has_rate_limit_msg, (
        f"Rate-limited response should indicate rate limiting via status_code=429 "
        f"or message containing 'rate', got: {result}"
    )


def test_eleventh_request_has_no_data():
    """Rate-limited response should NOT include processed data."""
    time_fn, _ = make_time_fn()
    for i in range(10):
        handle_request("client_h", {"action": f"req{i}"}, time_fn=time_fn)
    result = handle_request("client_h", {"action": "should_not_process"}, time_fn=time_fn)
    assert result["status"] == "error"
    assert "data" not in result or result.get("data") is None, (
        "Rate-limited response should not contain processed data"
    )


def test_rapid_burst_all_rejected_after_limit():
    """After hitting limit, ALL subsequent requests must be rejected until window resets."""
    time_fn, _ = make_time_fn()
    for i in range(10):
        handle_request("client_i", {"action": f"req{i}"}, time_fn=time_fn)

    # Requests 11, 12, 13 should ALL be rejected
    for i in range(3):
        result = handle_request("client_i", {"action": f"over{i}"}, time_fn=time_fn)
        assert result["status"] == "error", (
            f"Request {11+i} should be rejected but got status={result['status']}"
        )


def test_exactly_at_limit_succeeds():
    """The 10th request (exactly at limit) should still succeed."""
    time_fn, _ = make_time_fn()
    for i in range(9):
        handle_request("client_j", {"action": f"req{i}"}, time_fn=time_fn)
    result = handle_request("client_j", {"action": "tenth"}, time_fn=time_fn)
    assert result["status"] == "ok", "The 10th request should still succeed (limit is 10)"
    # But the 11th should fail
    result = handle_request("client_j", {"action": "eleventh"}, time_fn=time_fn)
    assert result["status"] == "error", "The 11th request should be rate limited"
