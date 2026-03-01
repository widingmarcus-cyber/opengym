# Challenge 230: Timestamp Normalization

## Objective

Normalize timestamps from multiple formats and timezones into a canonical UTC ISO-8601 format.

## Context

Events flowing into an observability pipeline come from systems across the globe, each using its own timestamp format and timezone. Before logs can be correlated, searched, or alerted on, timestamps must be normalized to a single canonical format. The industry standard is ISO-8601 in UTC: `YYYY-MM-DDTHH:MM:SSZ`.

## Task

Read `setup/events.json` which contains an array of event objects with timestamps in various formats:

1. **Unix epoch seconds**: `1704459600`
2. **Unix epoch milliseconds**: `1704459600000`
3. **ISO-8601 with offset**: `"2025-01-05T09:00:00-05:00"`
4. **ISO-8601 UTC**: `"2025-01-05T14:00:00Z"` (already correct)
5. **RFC 2822**: `"Sun, 05 Jan 2025 14:00:00 +0000"`
6. **Custom format**: `"05/Jan/2025 14:00:00 +0000"` (Apache-style)
7. **US format with timezone**: `"01/05/2025 09:00:00 AM EST"`

Write `setup/normalized.json` containing the same events but with all `timestamp` fields normalized to ISO-8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ`

Each output event should have the same fields as the input, with only the `timestamp` field changed.

## Requirements

- Parse ALL timestamp formats correctly
- Convert all timestamps to UTC
- Output format must be exactly `YYYY-MM-DDTHH:MM:SSZ` (no fractional seconds, no offset — just trailing Z)
- Preserve all other event fields unchanged
- Preserve event order

## Verification

```bash
python3 tests/verify.py
```
