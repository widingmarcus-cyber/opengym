You are the Deduplicator agent. Your task is to remove duplicate events from an event stream.

1. Read `setup/events.json`. It contains 8 events, some of which share the same `event_id`.
2. Deduplicate the events: keep only the first occurrence of each unique `event_id`.
3. Write the unique events to `setup/processed.json` as a JSON array.

Preserve the order of first occurrences. Each entry should keep its original `event_id` and `data` fields.
