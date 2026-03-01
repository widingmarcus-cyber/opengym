"""Tests for Challenge 078: LRU Cache."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from lru_cache import LRUCache


def test_basic_put_and_get():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_get_missing_key():
    cache = LRUCache(2)
    assert cache.get("x") == -1


def test_eviction_on_capacity():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.get("a") == -1
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_access_updates_order():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)
    assert cache.get("b") == -1
    assert cache.get("a") == 1


def test_overwrite_existing_key():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    assert cache.get("a") == 10
    assert cache.size() == 2


def test_size():
    cache = LRUCache(3)
    assert cache.size() == 0
    cache.put("a", 1)
    assert cache.size() == 1
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.size() == 3
    cache.put("d", 4)
    assert cache.size() == 3


def test_keys_order():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.keys() == ["c", "b", "a"]


def test_keys_after_access():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    cache.get("a")
    assert cache.keys() == ["a", "c", "b"]


def test_capacity_one():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == -1
    assert cache.get("b") == 2
    assert cache.size() == 1


def test_overwrite_does_not_evict():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 100)
    assert cache.get("a") == 100
    assert cache.get("b") == 2
    assert cache.size() == 2
