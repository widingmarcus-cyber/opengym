# Challenge 084: Text Redactor

## Difficulty: Easy

## Task

Implement a text redaction function that detects and replaces sensitive information with `[REDACTED]`. The function must handle several common patterns of personally identifiable information (PII).

## Requirements

Implement this function in `setup/redactor.py`:

1. `redact(text)` -- Takes a string and returns a new string with all sensitive information replaced by `[REDACTED]`. Must detect and redact:

   - **SSNs**: Format `XXX-XX-XXXX` where X is a digit (e.g., `123-45-6789`)
   - **Credit card numbers**: 16 digits, possibly separated by spaces or dashes in groups of 4 (e.g., `4111111111111111`, `4111-1111-1111-1111`, `4111 1111 1111 1111`)
   - **Email addresses**: Standard format `user@domain.tld` (e.g., `john.doe@example.com`)
   - **US phone numbers**: Various formats including `(555) 123-4567`, `555-123-4567`, `+1-555-123-4567`, `+1 (555) 123-4567`

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- Each detected PII instance should be replaced with exactly `[REDACTED]`
- Text that does not match PII patterns should be preserved unchanged
