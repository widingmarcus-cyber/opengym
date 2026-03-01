You are the Deduplicator agent. Your task is to remove duplicate events from an event stream.

1. Read `setup/events.json`. It contains 8 events, some of which share the same `event_id`.
2. Deduplicate the events: keep only the first occurrence of each unique `event_id`.
3. Write the unique events to `setup/processed.json` as a JSON array.

The unique event_ids are: e1, e2, e3, e4, e5 (5 unique events total).

Expected output in processed.json:
```json
[
  {"event_id": "e1", "data": "a"},
  {"event_id": "e2", "data": "b"},
  {"event_id": "e3", "data": "c"},
  {"event_id": "e4", "data": "d"},
  {"event_id": "e5", "data": "e"}
]
```
