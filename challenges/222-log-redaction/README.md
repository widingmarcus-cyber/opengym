# Challenge 222: Log Redaction

## Objective

Implement **log redaction** to mask sensitive data patterns in log output. The current logger writes raw data containing SSNs, credit card numbers, and email addresses without any masking.

## Setup

- `setup/logger.py` — A logging module with:
  - A `redact(text)` function that should mask sensitive patterns (currently returns text unchanged).
  - A `log_event(event_data)` function that logs event information (currently logs raw data).

## What You Must Do

1. Implement the `redact(text)` function to find and mask these patterns:
   - **SSNs**: Pattern `XXX-XX-XXXX` (e.g., `123-45-6789`) -> `***-**-****`
   - **Credit cards**: 16-digit numbers with optional dashes/spaces (e.g., `4111-1111-1111-1111` or `4111111111111111`) -> `****-****-****-XXXX` (keep last 4 digits)
   - **Email addresses**: Standard email pattern (e.g., `user@example.com`) -> `***@***.***`
2. Update `log_event(event_data)` to pass all string values through `redact()` before including them in the output.
3. The functions must handle:
   - Multiple sensitive values in the same string.
   - Nested sensitive data in dict values.
   - Strings with no sensitive data (return unchanged).

## Constraints

- Do NOT change function signatures.
- Use regex patterns for detection.
- SSN pattern: `\d{3}-\d{2}-\d{4}`
- Credit card pattern: `\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}`
- Email pattern: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
- The `redact` function must return a string.
