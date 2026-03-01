# Challenge 021: Implement Rate Limiter

## Difficulty: Hard

## Task

The file `setup/rate_limiter.py` is empty. Implement a `RateLimiter` class using the token bucket algorithm.

## Requirements

The `RateLimiter` class constructor accepts an optional `time_func` parameter (a callable returning the current time as a float, in seconds). If not provided, default to `time.time`.

### Methods

1. `configure(key, max_tokens, refill_rate)` — Configure rate limiting for a given key. `max_tokens` is the bucket capacity. `refill_rate` is tokens added per second. The bucket starts full
2. `allow(key)` — Consume one token for the given key. Return `True` if a token was available, `False` otherwise. If the key has not been configured, raise `ValueError`
3. `reset(key)` — Reset the bucket for a key back to full capacity. Raise `ValueError` if the key has not been configured

## Rules

- Only modify files in the `setup/` directory
- Tokens refill continuously based on elapsed time (not in discrete intervals)
- Tokens cannot exceed `max_tokens`
- The `time_func` parameter enables deterministic testing

## Examples

```python
import time

limiter = RateLimiter()
limiter.configure("api", max_tokens=5, refill_rate=1.0)

limiter.allow("api")  # True (4 tokens left)
limiter.allow("api")  # True (3 tokens left)

# After waiting, tokens refill
limiter.reset("api")  # Back to 5 tokens
```
