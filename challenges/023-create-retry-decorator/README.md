# Challenge 023: Create Retry Decorator

## Difficulty: Medium

## Task

The file `setup/retry.py` is empty. Implement a `retry` decorator that retries a function call on failure with exponential backoff.

## Requirements

The `retry` decorator accepts these parameters:

1. `max_attempts` (int, default 3) — Maximum number of attempts (including the first call)
2. `delay` (float, default 1.0) — Initial delay in seconds between retries
3. `backoff` (float, default 2.0) — Multiplier applied to the delay after each retry
4. `exceptions` (tuple, default `(Exception,)`) — Tuple of exception types to catch and retry on
5. `sleep_func` (callable, default `time.sleep`) — The function used for sleeping between retries, to enable deterministic testing

## Behavior

- On each call, if the function raises one of the specified exceptions, wait and retry
- The delay between the 1st and 2nd attempt is `delay`. Between 2nd and 3rd is `delay * backoff`. And so on
- If all attempts are exhausted, raise the last exception
- If the function succeeds, return its result immediately
- Only catch exceptions listed in `exceptions`; other exceptions propagate immediately

## Rules

- Only modify files in the `setup/` directory

## Examples

```python
@retry(max_attempts=3, delay=1.0, backoff=2.0)
def flaky():
    ...

@retry(max_attempts=5, exceptions=(ConnectionError, TimeoutError))
def call_api():
    ...
```
