# Challenge 159: Duplicate Event Handling

## Difficulty: Medium
## Category: Agent Collaboration
## Dimension: Multi-Agent

## Description

An event stream contains duplicate events (same event_id). An agent must deduplicate the events, keeping only unique entries, and count them. This tests idempotency handling -- a critical requirement in event-driven systems.

## Objective

- Process an event stream containing duplicates
- Deduplicate events by their event_id (keep first occurrence)
- Count the unique events

## Setup

- `setup/events.json` -- pre-created with 8 events, 3 of which are duplicates

## Steps

1. **Step 1 (Deduplicator):** Read `steps/step_1.md`. Deduplicate the events.
2. **Step 2 (Counter):** Read `steps/step_2.md`. Count unique events and write the answer.

## Verification

```bash
python tests/verify.py
```

Checks that processed.json has 5 unique events with no duplicate event_ids, and answer.txt = "5".
