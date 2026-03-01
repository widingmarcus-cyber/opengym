# Challenge 235: State Machine Execution

## Objective

Execute a state machine by processing a sequence of events. You must read the state machine definition and event sequence, then simulate the machine step-by-step and produce an execution trace showing every state transition.

## Setup

- `setup/state_machine.json` - Defines the state machine: initial state, states, and transitions (each with source, event, target, and optional guard condition).
- `setup/events.json` - An ordered list of events to process through the state machine.

## Task

1. Read the state machine definition from `setup/state_machine.json`.
2. Read the event sequence from `setup/events.json`.
3. Starting from the initial state, process each event:
   - Find a matching transition from the current state for the given event.
   - If a guard condition exists, evaluate it against the event's payload.
   - If no valid transition exists, the event is ignored (log it as "ignored").
   - If a valid transition exists, transition to the target state.
4. Write `setup/execution_trace.json` with the full trace of every event processed.

## Output Format

`setup/execution_trace.json`:
```json
{
  "initial_state": "<start state>",
  "final_state": "<end state>",
  "total_events": <number>,
  "transitions": [
    {
      "event": "<event_name>",
      "from_state": "<source>",
      "to_state": "<target>",
      "status": "transitioned" | "ignored",
      "step": <1-based index>
    },
    ...
  ]
}
```

## Guard Conditions

Some transitions have guard conditions like `{"field": "amount", "operator": "gt", "value": 100}`. The event payload must satisfy the guard for the transition to fire. Supported operators: `gt`, `lt`, `eq`, `gte`, `lte`.

## Constraints

- Process events strictly in order.
- If multiple transitions match, use the first one defined.
- If no transition matches the event from the current state, log it as "ignored" with `to_state` equal to the current state.
