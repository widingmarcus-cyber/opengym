# Challenge 166: 429 Retry-After Enforcement

## Objective

Call the rate-limited API tool and handle HTTP 429 responses by respecting the `Retry-After` header. Retrieve the successful result and write it to `setup/answer.txt`.

## Context

Real-world APIs enforce rate limits using HTTP 429 status codes with a `Retry-After` header indicating how long to wait before retrying. A robust agent must detect these responses, wait the specified duration, and retry — rather than giving up or hammering the endpoint.

## Tools

- `tools/api.py` — Simulates a rate-limited API endpoint. Returns JSON with status codes and headers.

## Instructions

1. Call `tools/api.py` to make an API request.
2. If the response status is `429`, read the `Retry-After` header value and wait that many seconds before retrying.
3. Continue retrying until you receive a `200` response.
4. Extract the `result` value from the successful response body.
5. Write that value to `setup/answer.txt`.

## Expected Behavior

- The tool will return 429 on the first 2 calls, then 200 on the third.
- The successful response body contains `{"result": "success_data_42"}`.
- `setup/answer.txt` should contain exactly: `success_data_42`
