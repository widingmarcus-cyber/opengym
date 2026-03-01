"""Regular expression validators."""

import re


def validate_email(email):
    """Validate basic email format.

    Valid: alphanumeric, dots, underscores, hyphens before @;
    domain with at least one dot and 2+ letter TLD.
    Example valid: user.name@example.com
    """
    pattern = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}"
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validate US phone number format: (XXX) XXX-XXXX.

    Example valid: (555) 123-4567
    """
    pattern = r"\(\d{3}\) \d{3}\-\d{4}"
    return bool(re.match(pattern, phone))


def validate_url(url):
    """Validate HTTP/HTTPS URL format.

    Must start with http:// or https:// and have a valid domain.
    Example valid: https://example.com/path
    """
    pattern = r"http://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/\S*)?"
    return bool(re.fullmatch(pattern, url))


def validate_date(date_str):
    """Validate date in YYYY-MM-DD format.

    Month must be 01-12, day must be 01-31.
    Example valid: 2024-01-15
    """
    pattern = r"\d{4}/\d{2}/\d{2}"
    return bool(re.fullmatch(pattern, date_str))


def validate_ipv4(ip):
    """Validate IPv4 address format.

    Each octet must be 0-255. No leading zeros (except '0' itself).
    Example valid: 192.168.1.1
    """
    pattern = r"(\d+)\.(\d+)\.(\d+)\.(\d+)"
    match = re.fullmatch(pattern, ip)
    if not match:
        return False
    for group in match.groups():
        value = int(group)
        if value > 255:
            return False
    return True
