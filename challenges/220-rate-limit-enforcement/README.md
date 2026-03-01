# Challenge 220: Rate Limit Enforcement

## Objective

Implement **rate limiting** for an API handler that currently allows unlimited requests. Without rate limiting, the API is vulnerable to denial-of-service and brute-force attacks.

## Setup

- `setup/api.py` — A module with:
  - A `RateLimiter` class (currently a stub that always allows requests).
  - A `handle_request(limiter, client_id, action)` function that processes API requests.
  - The rate limiter should enforce: **max 5 requests per 10-second window per client**.

## What You Must Do

1. Open `setup/api.py` and implement the `RateLimiter` class:
   - `is_allowed(client_id)` — Returns `True` if the client is within the rate limit, `False` otherwise.
   - `record_request(client_id)` — Records a request timestamp for the client.
   - The limit is **5 requests per 10 seconds** per client (sliding window).
2. Update `handle_request` to check the rate limiter before processing.
3. Behavior:
   - Requests within the limit return `{"status": "ok", "message": "..."}`.
   - Requests exceeding the limit return `{"status": "rate_limited", "message": "..."}`.
   - Different clients have independent limits.

## Constraints

- Do NOT change function signatures.
- Use a sliding window approach (based on timestamps, not fixed intervals).
- The `RateLimiter` must store timestamps per client and expire old ones.
- Default limit: 5 requests per 10 seconds. The `RateLimiter.__init__` should accept `max_requests` and `window_seconds` parameters.
