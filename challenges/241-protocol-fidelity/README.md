# Challenge 241: Protocol Fidelity Under State Explosion

## Difficulty: Hard
## Category: Long-Horizon
## Dimension: Planning

## Description

You are given a finite state machine (FSM) protocol specification and a sequence of events. For each event, you must evaluate guard conditions, execute the correct transition, and produce side effects.

The FSM processes records identified by an `id` field in each event payload. The machine tracks state per-event using a shared state object (not per-record state machines).

## Objective

Process all 25 events in order through the FSM. For each event:

1. Look up the current state in the protocol
2. Find the matching transition for the event type
3. If the transition has a guard, evaluate it against the current state
4. If the guard passes (or there is no guard), execute the transition:
   - Move to the new state
   - Execute the action (mutate state fields and create side-effect files)
5. If the guard fails, skip the event (do not transition, do not execute the action) but still log it as a "blocked" entry
6. Log the transition (or blocked attempt) to the execution log

## Input Files

- `setup/protocol.json` -- FSM definition with states and transitions
- `setup/guards.json` -- Guard condition definitions
- `setup/actions.json` -- Action definitions (state mutations and side effects)
- `setup/events.json` -- Ordered list of 25 events to process
- `setup/state.json` -- Initial state of the machine

## Guard Evaluation

Guards check a field in the current state using an operator:
- `not_null`: field is not null/None
- `gte`: field >= value
- `lt`: field < value
- `gt`: field > value
- `eq`: field == value

## Action Execution

Actions can:
- `set`: Set fields in the state to specific values. The special value `"current_event"` means use the current event's sequence number.
- `set_increment`: Increment a numeric field by the given amount.
- `reset`: If true, reset the state to initial values (but keep `records_processed`).
- `side_effect`: Create a file in `setup/side_effects/`. The filename and content may contain `{id}` which should be replaced with the `id` from the event payload.

After each action, increment `records_processed` by 1.

## Output Files

1. `setup/execution_log.json` -- Array of 25 entries, one per event. Each entry:
   ```json
   {
     "seq": 1,
     "event": "submit",
     "from_state": "IDLE",
     "to_state": "PROCESSING",
     "action": "log_submit",
     "blocked": false
   }
   ```
   For blocked events (guard failed):
   ```json
   {
     "seq": 5,
     "event": "resubmit",
     "from_state": "REJECTED",
     "to_state": "REJECTED",
     "action": null,
     "blocked": true
   }
   ```

2. `setup/final_state.json` -- The state object after all 25 events have been processed.

3. `setup/side_effects/` -- Directory containing any side-effect files created by actions.

## Verification

```bash
python tests/verify.py
```

Checks execution log correctness, final state, and side-effect files.
