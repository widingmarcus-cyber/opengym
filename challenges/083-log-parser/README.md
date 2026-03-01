# Challenge 083: Log Parser

## Difficulty: Easy

## Task

Parse structured log files and extract useful information. The file `setup/access.log` contains server log entries in a specific format, and you must implement parsing functions in `setup/log_parser.py`.

## Requirements

Implement these functions in `setup/log_parser.py`:

1. `parse_line(line)` -- Parse a single log line and return a dictionary with keys: `timestamp` (str), `level` (str), `service` (str), `message` (str). For example, parsing `"2024-01-15 10:30:00 [INFO] UserService: User logged in (user_id=42)"` should return `{"timestamp": "2024-01-15 10:30:00", "level": "INFO", "service": "UserService", "message": "User logged in (user_id=42)"}`.

2. `parse_file(filepath)` -- Read a log file and return a list of dictionaries (one per line), using `parse_line` for each line.

3. `count_by_level(entries)` -- Given a list of parsed entries, return a dictionary mapping each log level to its count. E.g., `{"INFO": 50, "WARN": 20, "ERROR": 10, "DEBUG": 25}`.

4. `errors_per_hour(entries)` -- Given a list of parsed entries, return a dictionary mapping each hour (as an integer 0-23) to the count of ERROR-level entries in that hour.

## Log Format

Each line in `setup/access.log` follows this pattern:

```
YYYY-MM-DD HH:MM:SS [LEVEL] ServiceName: Message text here
```

- `LEVEL` is one of: `INFO`, `WARN`, `ERROR`, `DEBUG`
- `ServiceName` is a single word (e.g., `UserService`, `AuthService`)
- `Message` is the remaining text after the colon and space

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- Do not use pandas or other external libraries
