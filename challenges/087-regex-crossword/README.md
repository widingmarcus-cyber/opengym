# Challenge 087: Regex Crossword

## Difficulty: Medium

## Task

Implement five functions in `setup/patterns.py`, each returning a regex pattern string that matches a specific format. The patterns will be compiled and tested with `re.fullmatch()`.

## Requirements

Each function must return a regex pattern string (not a compiled pattern). The pattern must match the entire input string (tested via `re.fullmatch`).

### 1. `match_ipv4()`

Match valid IPv4 addresses. Each octet must be a number from 0 to 255.

- Valid: `192.168.1.1`, `0.0.0.0`, `255.255.255.255`, `10.0.0.1`
- Invalid: `256.1.1.1`, `192.168.1`, `192.168.1.1.1`, `01.01.01.01`

### 2. `match_iso_date()`

Match dates in `YYYY-MM-DD` format. Year is 4 digits, month is 01-12, day is 01-31.

- Valid: `2024-01-15`, `1999-12-31`, `2000-06-01`
- Invalid: `2024-13-01`, `2024-00-15`, `2024-01-32`, `24-01-15`

### 3. `match_hex_color()`

Match hex color codes: `#RGB` (3 hex digits) or `#RRGGBB` (6 hex digits). Case-insensitive for hex digits.

- Valid: `#fff`, `#FF5733`, `#000`, `#abcdef`
- Invalid: `#ffff`, `#GG0000`, `fff`, `#12345`

### 4. `match_semantic_version()`

Match semantic version strings: `MAJOR.MINOR.PATCH` with optional pre-release suffix (`-alpha`, `-beta.1`, `-rc.2`, etc.).

- Valid: `1.0.0`, `0.1.0`, `12.34.56`, `1.0.0-alpha`, `2.1.3-beta.1`, `1.0.0-rc.2`
- Invalid: `1.0`, `1.0.0.0`, `v1.0.0`, `1.0.0-`

### 5. `match_quoted_string()`

Match strings enclosed in single or double quotes. The string may contain escaped quotes (`\"` inside double-quoted, `\'` inside single-quoted).

- Valid: `"hello"`, `'world'`, `"it\'s"` (but this is double-quoted so no issue), `"say \"hi\""`, `'don\'t'`
- Invalid: `"unclosed`, `'mixed"`, `hello`, `""extra"`

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- Each function returns a raw pattern string suitable for `re.fullmatch()`
