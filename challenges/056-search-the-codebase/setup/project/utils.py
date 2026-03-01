"""Utility functions."""

import re
import hashlib
import json


def validate_email(email):
    """Validate an email address format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def format_response(data, status="success"):
    """Format a standard API response."""
    return json.dumps({"status": status, "data": data})


def paginate(items, page, per_page):
    """Paginate a list of items."""
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]


# TODO: add input sanitization function
# TODO: add rate limiting helper
