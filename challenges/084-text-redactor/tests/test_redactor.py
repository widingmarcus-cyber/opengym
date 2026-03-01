"""Tests for Challenge 084: Text Redactor."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from redactor import redact


def test_redact_ssn():
    text = "My SSN is 123-45-6789 and it is private."
    result = redact(text)
    assert "123-45-6789" not in result
    assert "[REDACTED]" in result
    assert "My SSN is" in result


def test_redact_credit_card_no_separators():
    text = "Card number: 4111111111111111 for payment."
    result = redact(text)
    assert "4111111111111111" not in result
    assert "[REDACTED]" in result


def test_redact_credit_card_with_dashes():
    text = "Use card 4111-1111-1111-1111 for checkout."
    result = redact(text)
    assert "4111-1111-1111-1111" not in result
    assert "[REDACTED]" in result


def test_redact_credit_card_with_spaces():
    text = "Card: 5500 0000 0000 0004 is on file."
    result = redact(text)
    assert "5500 0000 0000 0004" not in result
    assert "[REDACTED]" in result


def test_redact_email():
    text = "Contact me at john.doe@example.com for details."
    result = redact(text)
    assert "john.doe@example.com" not in result
    assert "[REDACTED]" in result
    assert "Contact me at" in result


def test_redact_phone_with_parentheses():
    text = "Call me at (555) 123-4567 anytime."
    result = redact(text)
    assert "(555) 123-4567" not in result
    assert "[REDACTED]" in result


def test_redact_phone_with_dashes():
    text = "Phone: 555-123-4567 is my number."
    result = redact(text)
    assert "555-123-4567" not in result
    assert "[REDACTED]" in result


def test_redact_phone_with_country_code():
    text = "Reach me at +1-555-123-4567 for support."
    result = redact(text)
    assert "+1-555-123-4567" not in result
    assert "[REDACTED]" in result


def test_redact_mixed_content():
    text = (
        "Employee Jane Smith (SSN: 987-65-4321) can be reached at "
        "jane.smith@corp.org or (800) 555-0199. Her corporate card "
        "is 4222-2222-2222-2222."
    )
    result = redact(text)
    assert "987-65-4321" not in result
    assert "jane.smith@corp.org" not in result
    assert "(800) 555-0199" not in result
    assert "4222-2222-2222-2222" not in result
    assert result.count("[REDACTED]") == 4


def test_redact_preserves_non_sensitive_text():
    text = "The meeting is at 3pm on 2024-01-15 in room 404. Budget is $10,000."
    result = redact(text)
    assert result == text
