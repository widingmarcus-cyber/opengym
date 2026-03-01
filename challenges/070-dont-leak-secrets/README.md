# Challenge 070: Don't Leak Secrets

## Difficulty: Medium

## Task

The file `setup/logger.py` contains a `log_request` function that logs HTTP request details. Currently it logs everything verbatim, including sensitive data like Authorization headers, API keys in URLs, and passwords in request bodies.

Fix the logger to redact sensitive information before logging.

## Setup

- `setup/logger.py` — Contains the vulnerable logging function
- `setup/sample_requests.py` — Example request data for reference (do not modify)

## Requirements

Fix `log_request(method, url, headers, body)` so that:

1. Normal request details (method, non-sensitive URLs, safe headers) are still logged
2. The `Authorization` header value is redacted (masked)
3. API key parameters in URLs (e.g., `?api_key=...` or `&api_key=...`) are redacted
4. Password fields in the request body are redacted
5. The function returns the log string (for testability)
6. Redacted values should be replaced with `***REDACTED***`

## Rules

- Only modify `setup/logger.py`
- The function signature must remain `log_request(method, url, headers, body)`
- The function must return the formatted log string
