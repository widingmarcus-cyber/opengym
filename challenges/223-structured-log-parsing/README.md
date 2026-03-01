# Challenge 223: Structured Log Parsing

## Objective

Parse unstructured log lines from multiple formats into a single structured JSON output.

## Context

Production systems emit logs in many different formats — syslog, Apache access logs, and custom application formats. Observability pipelines need to parse these heterogeneous log lines into a unified structured format for querying and alerting.

## Task

Read `setup/logs.txt` which contains mixed-format log entries from three sources:

1. **Syslog format**: `<priority>timestamp hostname process[pid]: message`
   - Example: `<134>Jan  5 14:23:01 webserver01 nginx[2345]: connection accepted`

2. **Apache Combined Log Format**: `ip - - [timestamp] "method path protocol" status size "referer" "user-agent"`
   - Example: `192.168.1.50 - - [05/Jan/2025:14:23:05 +0000] "GET /api/health HTTP/1.1" 200 15 "-" "curl/7.68.0"`

3. **Custom application format**: `[LEVEL] timestamp | service | message | key=value key=value ...`
   - Example: `[ERROR] 2025-01-05T14:23:10Z | auth-service | login failed | user=admin attempt=3`

Write `setup/parsed_logs.json` containing a JSON array of objects. Each object must have these fields:

- `timestamp` — ISO-8601 UTC format (e.g., `"2025-01-05T14:23:01Z"`)
- `source` — one of `"syslog"`, `"apache"`, `"app"`
- `level` — log level: `"INFO"`, `"WARN"`, `"ERROR"`, or `"DEBUG"` (syslog and apache default to `"INFO"` unless message indicates otherwise)
- `message` — the core log message
- `metadata` — object with any additional extracted fields (hostname, IP, status code, service name, key-value pairs, etc.)

## Requirements

- Parse ALL lines from `logs.txt` (skip blank lines)
- Correctly identify the format of each line
- Extract timestamps and normalize to ISO-8601 UTC
- Preserve all meaningful data in the metadata field
- Output valid JSON

## Verification

```bash
python3 tests/verify.py
```
