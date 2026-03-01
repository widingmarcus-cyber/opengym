"""Input validation functions."""


def is_valid_email(email):
    """Check if email has valid basic format."""
    if "@" not in email:
        return False
    parts = email.split("@")
    local = parts[0]
    domain = parts[1]
    if not local or not domain:
        return False
    if "." not in domain:
        return False
    return True


def is_palindrome(s):
    """Check if string is a palindrome (case-insensitive, ignoring non-alphanumeric)."""
    cleaned = s.lower()
    return cleaned == cleaned[::-1]


def is_valid_password(password):
    """Check if password meets requirements."""
    if len(password) < 8:
        return False
    has_upper = False
    has_lower = False
    has_digit = False
    for char in password:
        if char.isupper():
            has_upper = True
        if char.islower():
            has_lower = True
        if char.isdigit():
            has_digit = True
    return has_upper or has_lower or has_digit


def flatten_list(nested):
    """Flatten a nested list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result
