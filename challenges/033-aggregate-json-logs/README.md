# Challenge 033: Aggregate JSON Logs

## Difficulty: Easy

## Task

Parse a JSONL (one JSON object per line) log file and compute summary statistics. The file `setup/logs.jsonl` contains log entries, and you must implement the analysis functions in `setup/analyzer.py`.

## Requirements

Implement these functions in `setup/analyzer.py`:

1. `count_by_level(filepath)` -- Read the JSONL file and return a dictionary mapping each log level to its count. E.g., `{"INFO": 25, "WARN": 10, "ERROR": 5}`.
2. `error_rate(filepath)` -- Return the proportion of ERROR-level entries as a float between 0 and 1.
3. `busiest_hour(filepath)` -- Return the hour (0-23) that has the most log entries based on the timestamp field.
4. `messages_containing(filepath, keyword)` -- Return a list of message strings that contain the given keyword (case-insensitive match).

## Data Format

Each line in `setup/logs.jsonl` is a JSON object with:
- `timestamp`: ISO 8601 format, e.g., `"2024-01-15T10:30:00"`
- `level`: One of `"INFO"`, `"WARN"`, `"ERROR"`
- `message`: A descriptive string

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules (json, etc.)
- Do not use pandas or other external libraries
