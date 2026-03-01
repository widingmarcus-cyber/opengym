# Challenge 014: Fix the Broken Regexes

## Difficulty: Medium

## Task

The file `setup/patterns.py` contains five validation functions, each using a regular expression. Every regex has a subtle bug that causes it to accept invalid input or reject valid input.

**Your job:** Fix the regular expressions so each validator works correctly.

## Functions

1. `validate_email(email)` -- Returns True if the string is a valid email (alphanumeric/dots/underscores before @, domain with dot)
2. `validate_phone(phone)` -- Returns True for US phone format: (XXX) XXX-XXXX
3. `validate_url(url)` -- Returns True for http:// or https:// URLs with a domain
4. `validate_date(date_str)` -- Returns True for dates in YYYY-MM-DD format (basic format check, month 01-12, day 01-31)
5. `validate_ipv4(ip)` -- Returns True for valid IPv4 addresses (four octets, each 0-255)

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- Each function must use `re.fullmatch()` (match the entire string, not a substring)
- Only fix the regex patterns; do not rewrite the validation logic
