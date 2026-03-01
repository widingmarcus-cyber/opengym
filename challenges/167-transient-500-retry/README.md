# Challenge 167: Transient 500 Retry

## Objective

Call the service tool and handle a transient HTTP 500 error by retrying. Write the successful result to `setup/answer.txt`.

## Context

Server errors (HTTP 500) are often transient — the service may recover on the next request. A robust agent should retry on 5xx errors with the expectation that the issue may resolve itself, unlike 4xx errors which indicate a client-side problem.

## Tools

- `tools/service.py` — Simulates a service that fails once then recovers.

## Instructions

1. Call `tools/service.py`.
2. If the response status is `500`, retry the call.
3. Extract the `value` from the successful response data.
4. Write that value to `setup/answer.txt`.

## Expected Behavior

- First call returns `{"status": 500, "error": "Internal Server Error"}`.
- Second call returns `{"status": 200, "data": {"value": "recovered_result"}}`.
- `setup/answer.txt` should contain exactly: `recovered_result`
