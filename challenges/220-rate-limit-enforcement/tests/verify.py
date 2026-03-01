import json
import os
import sys
import time

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from api import RateLimiter, handle_request


def test_requests_within_limit():
    """Requests within the limit should succeed."""
    limiter = RateLimiter(max_requests=5, window_seconds=10)
    for i in range(5):
        result = handle_request(limiter, "client_a", "get_data")
        if result.get("status") != "ok":
            print(json.dumps({"test": "requests_within_limit", "passed": False,
                              "message": f"Request {i+1} of 5 was rejected: {result}"}))
            return
    print(json.dumps({"test": "requests_within_limit", "passed": True, "message": "OK"}))


def test_requests_exceed_limit():
    """The 6th request from the same client within the window must be rate-limited."""
    limiter = RateLimiter(max_requests=5, window_seconds=10)
    # Make 5 allowed requests
    for i in range(5):
        handle_request(limiter, "client_b", "get_data")
    # 6th request should be rate-limited
    result = handle_request(limiter, "client_b", "get_data")
    if result.get("status") != "rate_limited":
        print(json.dumps({"test": "requests_exceed_limit", "passed": False,
                          "message": f"6th request was NOT rate-limited: {result}"}))
        return
    print(json.dumps({"test": "requests_exceed_limit", "passed": True, "message": "OK"}))


def test_different_clients_independent():
    """Different clients should have independent rate limits."""
    limiter = RateLimiter(max_requests=3, window_seconds=10)
    # Exhaust client_c's limit
    for i in range(3):
        handle_request(limiter, "client_c", "action")
    # client_c should be limited
    result_c = handle_request(limiter, "client_c", "action")
    if result_c.get("status") != "rate_limited":
        print(json.dumps({"test": "different_clients_independent", "passed": False,
                          "message": f"client_c was not rate-limited after 3 requests: {result_c}"}))
        return
    # client_d should still be allowed
    result_d = handle_request(limiter, "client_d", "action")
    if result_d.get("status") != "ok":
        print(json.dumps({"test": "different_clients_independent", "passed": False,
                          "message": f"client_d was incorrectly rate-limited: {result_d}"}))
        return
    print(json.dumps({"test": "different_clients_independent", "passed": True, "message": "OK"}))


def test_window_expiry():
    """Requests should be allowed again after the window expires."""
    limiter = RateLimiter(max_requests=2, window_seconds=1)
    # Make 2 requests (exhaust limit)
    handle_request(limiter, "client_e", "action")
    handle_request(limiter, "client_e", "action")
    # Should be limited now
    result = handle_request(limiter, "client_e", "action")
    if result.get("status") != "rate_limited":
        print(json.dumps({"test": "window_expiry", "passed": False,
                          "message": f"3rd request was not rate-limited: {result}"}))
        return
    # Wait for window to expire
    time.sleep(1.2)
    # Should be allowed again
    result2 = handle_request(limiter, "client_e", "action")
    if result2.get("status") != "ok":
        print(json.dumps({"test": "window_expiry", "passed": False,
                          "message": f"Request after window expiry was still limited: {result2}"}))
        return
    print(json.dumps({"test": "window_expiry", "passed": True, "message": "OK"}))


def test_handle_request_uses_limiter():
    """handle_request must actually check the rate limiter."""
    source_path = os.path.join(CHALLENGE_DIR, "setup", "api.py")
    with open(source_path, "r") as f:
        source = f.read()
    if "is_allowed" not in source or "record_request" not in source:
        print(json.dumps({"test": "handle_request_uses_limiter", "passed": False,
                          "message": "handle_request does not call is_allowed/record_request on the limiter"}))
        return
    # Check that handle_request references the limiter
    # Find the handle_request function body
    in_func = False
    uses_limiter = False
    for line in source.split("\n"):
        if "def handle_request" in line:
            in_func = True
            continue
        if in_func:
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                break
            if "limiter" in line and ("is_allowed" in line or "record_request" in line):
                uses_limiter = True
    if not uses_limiter:
        print(json.dumps({"test": "handle_request_uses_limiter", "passed": False,
                          "message": "handle_request body does not use the limiter parameter"}))
        return
    print(json.dumps({"test": "handle_request_uses_limiter", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_requests_within_limit()
    test_requests_exceed_limit()
    test_different_clients_independent()
    test_window_expiry()
    test_handle_request_uses_limiter()
