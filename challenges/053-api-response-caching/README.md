# Challenge 053: API Response Caching

## Difficulty: Medium

## Task

Implement a TTL-based caching layer for an API client. The file `setup/cached_client.py` contains a stub that needs to be completed.

## Setup

`setup/api.py` provides a `FakeAPI` class that simulates an API. Its `get(key)` method returns data and internally increments a call counter accessible via `api.call_count`.

## Requirements

Implement a `CachedClient` class in `setup/cached_client.py`:

### Constructor

`CachedClient(api, ttl, time_fn=None)` — Wraps the given API with a cache. `ttl` is the time-to-live in seconds. `time_fn` is an optional callable returning the current time as a float (defaults to `time.time`).

### Methods

1. `get(key)` — Return the cached result if the TTL has not expired, otherwise call the underlying API and cache the result.
2. `invalidate(key)` — Remove a specific key from the cache.
3. `clear()` — Remove all entries from the cache.
4. `stats()` — Return a dictionary `{"hits": int, "misses": int}` tracking cache performance.

## Rules

- Only modify files in the `setup/` directory (do not modify `api.py`)
- A cache miss occurs when a key is not in the cache or has expired
- A cache hit occurs when a valid (non-expired) cached value is returned
