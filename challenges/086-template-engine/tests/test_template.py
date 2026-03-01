"""Tests for Challenge 086: Template Engine."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from template import render


def test_simple_variable_substitution():
    template = "Hello, {{name}}!"
    result = render(template, {"name": "World"})
    assert result == "Hello, World!"


def test_multiple_variables():
    template = "{{greeting}}, {{name}}! Welcome to {{place}}."
    context = {"greeting": "Hi", "name": "Alice", "place": "Wonderland"}
    result = render(template, context)
    assert result == "Hi, Alice! Welcome to Wonderland."


def test_dot_notation():
    template = "User: {{user.name}}, Email: {{user.email}}"
    context = {"user": {"name": "Bob", "email": "bob@test.com"}}
    result = render(template, context)
    assert result == "User: Bob, Email: bob@test.com"


def test_missing_variable_renders_empty():
    template = "Hello, {{name}}! Your role is {{role}}."
    result = render(template, {"name": "Charlie"})
    assert result == "Hello, Charlie! Your role is ."


def test_if_true_condition():
    template = "{% if logged_in %}Welcome back!{% endif %}"
    result = render(template, {"logged_in": True})
    assert result == "Welcome back!"


def test_if_false_condition():
    template = "{% if logged_in %}Welcome back!{% endif %}"
    result = render(template, {"logged_in": False})
    assert result == ""


def test_if_else():
    template = "{% if premium %}Premium user{% else %}Free user{% endif %}"
    assert render(template, {"premium": True}) == "Premium user"
    assert render(template, {"premium": False}) == "Free user"


def test_for_loop():
    template = "Items: {% for item in items %}{{item}} {% endfor %}"
    result = render(template, {"items": ["apple", "banana", "cherry"]})
    assert result == "Items: apple banana cherry "


def test_nested_loop_in_conditional():
    template = (
        "{% if show_list %}"
        "List: {% for x in items %}{{x}}, {% endfor %}"
        "{% endif %}"
    )
    result = render(template, {"show_list": True, "items": ["a", "b", "c"]})
    assert result == "List: a, b, c, "
    result_hidden = render(template, {"show_list": False, "items": ["a", "b"]})
    assert result_hidden == ""


def test_variable_whitespace_flexibility():
    template = "{{ name }} and {{name}}"
    result = render(template, {"name": "test"})
    assert result == "test and test"
