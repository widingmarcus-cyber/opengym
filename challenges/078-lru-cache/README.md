# Challenge 078: LRU Cache

## Difficulty: Medium

## Task

The file `setup/lru_cache.py` contains a stub. Implement an `LRUCache` class that provides a Least Recently Used cache with O(1) time complexity for both `get` and `put` operations.

## Requirements

The `LRUCache` class must support:

1. `__init__(capacity: int)` -- Initialize the cache with a positive integer capacity.
2. `get(key) -> value` -- Return the value associated with `key` if it exists, otherwise return `-1`. Accessing a key makes it the most recently used.
3. `put(key, value)` -- Insert or update the value for `key`. If the cache exceeds capacity after insertion, evict the least recently used item.
4. `size() -> int` -- Return the current number of items in the cache.
5. `keys() -> list` -- Return keys in LRU order with the most recently used first.

## Rules

- Only modify files in the `setup/` directory
- Both `get` and `put` must operate in O(1) average time
- Do not use `functools.lru_cache`

## Examples

```python
cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")       # 1 (now "a" is most recent)
cache.put("c", 3)    # evicts "b" (least recently used)
cache.get("b")       # -1 (was evicted)
cache.keys()         # ["c", "a"]
cache.size()         # 2
```
