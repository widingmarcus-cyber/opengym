"""Tests for Challenge 005: Fix the Logic Bug."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from validators import is_valid_email, is_palindrome, is_valid_password, flatten_list


# --- Email validation ---

def test_email_valid():
    assert is_valid_email("user@example.com") is True
    assert is_valid_email("test.user@domain.org") is True


def test_email_no_at():
    assert is_valid_email("invalid") is False


def test_email_no_domain_dot():
    assert is_valid_email("user@localhost") is False


def test_email_multiple_at():
    assert is_valid_email("user@@example.com") is False
    assert is_valid_email("us@er@example.com") is False


def test_email_empty_parts():
    assert is_valid_email("@example.com") is False
    assert is_valid_email("user@") is False


# --- Palindrome ---

def test_palindrome_simple():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False


def test_palindrome_case_insensitive():
    assert is_palindrome("Racecar") is True


def test_palindrome_with_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_palindrome_with_punctuation():
    assert is_palindrome("Was it a car or a cat I saw?") is True


# --- Password validation ---

def test_password_valid():
    assert is_valid_password("Secret123") is True
    assert is_valid_password("MyP4ssword") is True


def test_password_too_short():
    assert is_valid_password("Ab1") is False


def test_password_no_uppercase():
    assert is_valid_password("lowercase1") is False


def test_password_no_lowercase():
    assert is_valid_password("UPPERCASE1") is False


def test_password_no_digit():
    assert is_valid_password("NoDigitsHere") is False


# --- Flatten list ---

def test_flatten_simple():
    assert flatten_list([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_flatten_deep():
    assert flatten_list([1, [2, [3, [4]]]]) == [1, 2, 3, 4]


def test_flatten_empty():
    assert flatten_list([]) == []
    assert flatten_list([[], []]) == []


def test_flatten_already_flat():
    assert flatten_list([1, 2, 3]) == [1, 2, 3]


# --- Additional bug-targeting tests ---

def test_email_multiple_at_with_dots():
    """Multiple @ where the second part has dots should still be invalid."""
    assert is_valid_email("user@sub.domain@evil.com") is False


def test_palindrome_spaces_simple():
    assert is_palindrome("a b a") is True


def test_palindrome_numbers_and_spaces():
    assert is_palindrome("1 2 1") is True


def test_password_missing_digit():
    assert is_valid_password("ABCDefgh") is False


def test_password_missing_lowercase():
    assert is_valid_password("ABCD1234") is False


def test_password_missing_uppercase():
    assert is_valid_password("abcd1234") is False


def test_flatten_mixed_depth():
    assert flatten_list([1, [2, [3]], [4]]) == [1, 2, 3, 4]


def test_flatten_five_deep():
    assert flatten_list([[[[[1]]]]]) == [1]


def test_email_at_sign_in_domain():
    """Email with @ in the domain part should be invalid."""
    assert is_valid_email("a@b.c@d.e") is False


def test_palindrome_with_exclamation():
    """Palindrome check should ignore non-alphanumeric characters."""
    assert is_palindrome("Able, was I ere I saw Elba!") is True


def test_flatten_triple_nested():
    """Flatten should handle triple-nested lists."""
    assert flatten_list([[[1, 2], 3], 4]) == [1, 2, 3, 4]
