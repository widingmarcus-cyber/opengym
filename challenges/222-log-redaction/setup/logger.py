"""
Logging module with sensitive data redaction.
VULNERABILITY: The logger outputs raw sensitive data (SSNs, credit cards,
emails) without any masking or redaction.
"""


def redact(text):
    """
    Redact sensitive patterns in text.

    Should mask:
    - SSNs (XXX-XX-XXXX) -> ***-**-****
    - Credit card numbers (16 digits) -> ****-****-****-XXXX (keep last 4)
    - Email addresses -> ***@***.***

    Args:
        text: The input string to redact.

    Returns:
        The redacted string.
    """
    # BUG: No redaction — returns text as-is
    return text


def log_event(event_data):
    """
    Log an event, redacting sensitive information from string values.

    Args:
        event_data: A dict containing event information.

    Returns:
        A dict with the same keys but string values redacted.
    """
    # BUG: Logs raw data without redaction
    output = {}
    for key, value in event_data.items():
        output[key] = value
    return output
