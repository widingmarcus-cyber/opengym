"""Tests for Challenge 018: Implement Stack."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from stack import Stack


def test_push_and_pop():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1


def test_pop_empty_raises():
    s = Stack()
    try:
        s.pop()
        assert False, "Expected IndexError"
    except IndexError:
        pass


def test_peek():
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.peek() == "b"
    assert s.peek() == "b"


def test_peek_empty_raises():
    s = Stack()
    try:
        s.peek()
        assert False, "Expected IndexError"
    except IndexError:
        pass


def test_is_empty_true():
    s = Stack()
    assert s.is_empty() is True


def test_is_empty_false():
    s = Stack()
    s.push(42)
    assert s.is_empty() is False


def test_size():
    s = Stack()
    assert s.size() == 0
    s.push(1)
    s.push(2)
    assert s.size() == 2
    s.pop()
    assert s.size() == 1


def test_iter_top_to_bottom():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert list(s) == [3, 2, 1]


def test_mixed_types():
    s = Stack()
    s.push(1)
    s.push("hello")
    s.push([1, 2, 3])
    assert s.pop() == [1, 2, 3]
    assert s.pop() == "hello"
    assert s.pop() == 1


def test_push_pop_push():
    s = Stack()
    s.push(10)
    s.push(20)
    s.pop()
    s.push(30)
    assert s.peek() == 30
    assert s.size() == 2
    assert list(s) == [30, 10]
