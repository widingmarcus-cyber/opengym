"""Tests for Challenge 024: Implement Event Emitter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from event_emitter import EventEmitter


def test_on_and_emit():
    emitter = EventEmitter()
    results = []
    emitter.on("event", lambda x: results.append(x))
    emitter.emit("event", 42)
    assert results == [42]


def test_multiple_listeners():
    emitter = EventEmitter()
    results = []
    emitter.on("event", lambda: results.append("a"))
    emitter.on("event", lambda: results.append("b"))
    emitter.emit("event")
    assert results == ["a", "b"]


def test_emit_with_no_listeners():
    emitter = EventEmitter()
    emitter.emit("nothing")


def test_off_removes_listener():
    emitter = EventEmitter()
    results = []
    callback = lambda: results.append("called")
    emitter.on("event", callback)
    emitter.off("event", callback)
    emitter.emit("event")
    assert results == []


def test_off_nonexistent_does_nothing():
    emitter = EventEmitter()
    callback = lambda: None
    emitter.off("event", callback)


def test_once_fires_once():
    emitter = EventEmitter()
    results = []
    emitter.once("event", lambda: results.append("fired"))
    emitter.emit("event")
    emitter.emit("event")
    assert results == ["fired"]


def test_once_with_args():
    emitter = EventEmitter()
    results = []
    emitter.once("data", lambda x, y: results.append((x, y)))
    emitter.emit("data", 1, 2)
    emitter.emit("data", 3, 4)
    assert results == [(1, 2)]


def test_on_returns_self():
    emitter = EventEmitter()
    result = emitter.on("event", lambda: None)
    assert result is emitter


def test_chaining():
    emitter = EventEmitter()
    results = []
    emitter.on("a", lambda: results.append("a")).on("b", lambda: results.append("b"))
    emitter.emit("a")
    emitter.emit("b")
    assert results == ["a", "b"]


def test_emit_with_kwargs():
    emitter = EventEmitter()
    results = []
    emitter.on("event", lambda name="": results.append(name))
    emitter.emit("event", name="Alice")
    assert results == ["Alice"]
