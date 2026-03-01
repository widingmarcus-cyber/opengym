# Challenge 239: Event Sourcing Rebuild

## Objective

Rebuild the current state of a system from an event sourcing log. The event log contains create, update, and delete operations for multiple entity types. You must replay all events in order and produce the final state of every entity.

## Setup

- `setup/events.json` - An ordered event log with create, update, and delete events for entities (users, products, orders).

## Task

1. Read `setup/events.json` containing the full event log.
2. Replay all events in chronological order:
   - **create**: Create a new entity with the given fields.
   - **update**: Update specific fields of an existing entity. Only overwrite the fields specified in the event data; preserve all other fields.
   - **delete**: Remove the entity from the current state. Mark it as deleted.
3. Write `setup/current_state.json` with the final state of all entities (grouped by entity type).
4. Write `setup/replay_summary.json` with statistics about the replay.

## Output Format

`setup/current_state.json`:
```json
{
  "users": {
    "<user_id>": { ... fields ... },
    ...
  },
  "products": {
    "<product_id>": { ... fields ... },
    ...
  },
  "orders": {
    "<order_id>": { ... fields ... },
    ...
  }
}
```

`setup/replay_summary.json`:
```json
{
  "total_events": <number>,
  "events_by_type": {
    "create": <count>,
    "update": <count>,
    "delete": <count>
  },
  "entities_by_type": {
    "users": {"active": <count>, "deleted": <count>},
    "products": {"active": <count>, "deleted": <count>},
    "orders": {"active": <count>, "deleted": <count>}
  }
}
```

## Constraints

- Deleted entities should NOT appear in `current_state.json`.
- If an update event targets a deleted entity, it should be ignored.
- If a create event uses an ID that already exists, treat it as an error and skip it.
- Events must be processed in the order they appear in the log.
