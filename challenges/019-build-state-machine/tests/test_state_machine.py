"""Tests for Challenge 019: Build State Machine."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from state_machine import StateMachine


def test_add_state_and_set_initial():
    sm = StateMachine()
    sm.add_state("idle")
    sm.set_initial("idle")
    assert sm.current_state == "idle"


def test_simple_transition():
    sm = StateMachine()
    sm.add_state("off")
    sm.add_state("on")
    sm.add_transition("off", "toggle", "on")
    sm.set_initial("off")
    result = sm.trigger("toggle")
    assert result == "on"
    assert sm.current_state == "on"


def test_multiple_transitions():
    sm = StateMachine()
    sm.add_state("locked")
    sm.add_state("unlocked")
    sm.add_transition("locked", "coin", "unlocked")
    sm.add_transition("unlocked", "push", "locked")
    sm.set_initial("locked")
    sm.trigger("coin")
    assert sm.current_state == "unlocked"
    sm.trigger("push")
    assert sm.current_state == "locked"


def test_invalid_event_raises():
    sm = StateMachine()
    sm.add_state("idle")
    sm.set_initial("idle")
    with pytest.raises(ValueError):
        sm.trigger("nonexistent")


def test_trigger_without_initial_raises():
    sm = StateMachine()
    sm.add_state("idle")
    with pytest.raises(ValueError):
        sm.trigger("go")


def test_set_initial_invalid_state_raises():
    sm = StateMachine()
    with pytest.raises(ValueError):
        sm.set_initial("nonexistent")


def test_add_transition_invalid_from_raises():
    sm = StateMachine()
    sm.add_state("on")
    with pytest.raises(ValueError):
        sm.add_transition("off", "toggle", "on")


def test_add_transition_invalid_to_raises():
    sm = StateMachine()
    sm.add_state("off")
    with pytest.raises(ValueError):
        sm.add_transition("off", "toggle", "on")


def test_get_valid_events():
    sm = StateMachine()
    sm.add_state("a")
    sm.add_state("b")
    sm.add_state("c")
    sm.add_transition("a", "go_b", "b")
    sm.add_transition("a", "go_c", "c")
    sm.set_initial("a")
    events = sm.get_valid_events()
    assert sorted(events) == ["go_b", "go_c"]


def test_self_transition():
    sm = StateMachine()
    sm.add_state("running")
    sm.add_transition("running", "tick", "running")
    sm.set_initial("running")
    result = sm.trigger("tick")
    assert result == "running"
    assert sm.current_state == "running"
