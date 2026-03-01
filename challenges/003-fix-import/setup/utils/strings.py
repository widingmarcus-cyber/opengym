"""String utility functions."""


def reverse_string(s):
    """Reverse a string."""
    return s[::-1]


def capitalize_words(s):
    """Capitalize the first letter of each word."""
    return " ".join(word.capitalize() for word in s.split())
