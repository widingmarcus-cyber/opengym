import json
import os
import sys
import re

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(CHALLENGE_DIR, "setup"))

from logger import redact, log_event


def test_ssn_redacted():
    """SSN pattern (XXX-XX-XXXX) must be masked."""
    text = "User SSN is 123-45-6789 on file."
    result = redact(text)
    if "123-45-6789" in result:
        print(json.dumps({"test": "ssn_redacted", "passed": False,
                          "message": f"SSN was NOT redacted: '{result}'"}))
        return
    if "***-**-****" not in result:
        print(json.dumps({"test": "ssn_redacted", "passed": False,
                          "message": f"Expected '***-**-****' placeholder in: '{result}'"}))
        return
    print(json.dumps({"test": "ssn_redacted", "passed": True, "message": "OK"}))


def test_credit_card_redacted():
    """Credit card numbers must be masked, keeping only last 4 digits."""
    text = "Card: 4111-1111-1111-1234 on file."
    result = redact(text)
    if "4111-1111-1111-1234" in result:
        print(json.dumps({"test": "credit_card_redacted", "passed": False,
                          "message": f"Credit card was NOT redacted: '{result}'"}))
        return
    if "1234" not in result:
        print(json.dumps({"test": "credit_card_redacted", "passed": False,
                          "message": f"Last 4 digits should be preserved: '{result}'"}))
        return
    # Also test without dashes
    text2 = "Card: 4111111111111234 on file."
    result2 = redact(text2)
    if "4111111111111234" in result2:
        print(json.dumps({"test": "credit_card_redacted", "passed": False,
                          "message": f"Credit card without dashes was NOT redacted: '{result2}'"}))
        return
    print(json.dumps({"test": "credit_card_redacted", "passed": True, "message": "OK"}))


def test_email_redacted():
    """Email addresses must be masked."""
    text = "Contact: alice@example.com for details."
    result = redact(text)
    if "alice@example.com" in result:
        print(json.dumps({"test": "email_redacted", "passed": False,
                          "message": f"Email was NOT redacted: '{result}'"}))
        return
    if "***@***.***" not in result:
        print(json.dumps({"test": "email_redacted", "passed": False,
                          "message": f"Expected '***@***.***' placeholder in: '{result}'"}))
        return
    print(json.dumps({"test": "email_redacted", "passed": True, "message": "OK"}))


def test_log_event_redacts_values():
    """log_event must redact sensitive data in string values."""
    event = {
        "user": "Alice",
        "ssn": "987-65-4321",
        "card": "5500-0000-0000-0004",
        "email": "alice@secret.org",
        "action": "login",
    }
    result = log_event(event)
    # SSN should be redacted
    if "987-65-4321" in str(result.get("ssn", "")):
        print(json.dumps({"test": "log_event_redacts_values", "passed": False,
                          "message": f"SSN not redacted in log_event output: {result}"}))
        return
    # Card should be redacted
    if "5500-0000-0000-0004" in str(result.get("card", "")):
        print(json.dumps({"test": "log_event_redacts_values", "passed": False,
                          "message": f"Card not redacted in log_event output: {result}"}))
        return
    # Email should be redacted
    if "alice@secret.org" in str(result.get("email", "")):
        print(json.dumps({"test": "log_event_redacts_values", "passed": False,
                          "message": f"Email not redacted in log_event output: {result}"}))
        return
    # Non-sensitive values should remain
    if result.get("user") != "Alice" or result.get("action") != "login":
        print(json.dumps({"test": "log_event_redacts_values", "passed": False,
                          "message": f"Non-sensitive values were modified: {result}"}))
        return
    print(json.dumps({"test": "log_event_redacts_values", "passed": True, "message": "OK"}))


def test_no_sensitive_data_unchanged():
    """Strings with no sensitive data should be returned unchanged."""
    text = "This is a normal log message with no secrets."
    result = redact(text)
    if result != text:
        print(json.dumps({"test": "no_sensitive_data_unchanged", "passed": False,
                          "message": f"Non-sensitive text was modified: '{result}'"}))
        return
    print(json.dumps({"test": "no_sensitive_data_unchanged", "passed": True, "message": "OK"}))


if __name__ == "__main__":
    test_ssn_redacted()
    test_credit_card_redacted()
    test_email_redacted()
    test_log_event_redacts_values()
    test_no_sensitive_data_unchanged()
