# Challenge 072: Rate Limit Endpoint

## Difficulty: Medium

## Task

The file `setup/handler.py` contains a `handle_request` function that processes API requests with no rate limiting. Add rate limiting so that each client is limited to 10 requests per 60-second window.

## Setup

- `setup/handler.py` — Contains the request handler that needs rate limiting
- `setup/rate_limiter.py` — Stub for the rate limiter (implement here or in handler.py)

## Requirements

Implement rate limiting so that:

1. Each client (identified by `client_id`) is limited to 10 requests per 60-second window
2. Requests within the limit return `{"status": "ok", "data": ...}`
3. Requests exceeding the limit return `{"status": "error", "message": "Rate limit exceeded"}`
4. Different clients have independent rate limits
5. Rate limits reset after the time window passes
6. The `handle_request` function accepts an optional `time_fn` parameter (a callable returning the current time as a float) for deterministic testing. If not provided, use `time.time`.

## Rules

- Modify `setup/handler.py` and/or `setup/rate_limiter.py`
- The function signature must be `handle_request(client_id, request, time_fn=None)`
- Do not use external rate-limiting libraries
