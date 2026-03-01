# Challenge 193: Timezone Drift

**Difficulty:** medium
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

Events are scheduled across different timezones. To properly coordinate them, all event times need to be normalized to UTC. Parse the timezone offsets and convert each event to its UTC equivalent.

## Objectives

- Read `setup/events.json` which contains events with times in different timezones.
- Convert all event times to UTC.
- Write `setup/answer.json` with all events normalized to UTC times.

## Data

Events:
- meeting: 2024-06-15T10:00:00Z (UTC) -> 10:00 UTC
- deploy: 2024-06-15T10:00:00-05:00 (US/Central) -> 15:00 UTC
- standup: 2024-06-15T10:00:00+09:00 (Asia/Tokyo) -> 01:00 UTC

## Expected Output

`setup/answer.json`:
```json
[
  {"event": "meeting", "utc_time": "2024-06-15T10:00:00Z"},
  {"event": "deploy", "utc_time": "2024-06-15T15:00:00Z"},
  {"event": "standup", "utc_time": "2024-06-15T01:00:00Z"}
]
```
