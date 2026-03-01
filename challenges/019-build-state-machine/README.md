# Challenge 019: Build State Machine

## Difficulty: Medium

## Task

The file `setup/state_machine.py` is empty. Implement a `StateMachine` class that models a finite state machine with named states and event-driven transitions.

## Requirements

The `StateMachine` class must support:

1. `add_state(name)` — Register a state by name
2. `add_transition(from_state, event, to_state)` — Define a transition from one state to another on a given event
3. `set_initial(state)` — Set the initial (current) state
4. `trigger(event)` — Process an event, transitioning to the appropriate state. Return the new state name. Raise `ValueError` if the event is not valid for the current state
5. `current_state` — Property that returns the name of the current state
6. `get_valid_events()` — Return a list of events valid for the current state

## Rules

- Only modify files in the `setup/` directory
- `add_transition` should raise `ValueError` if either `from_state` or `to_state` has not been added
- `set_initial` should raise `ValueError` if the state has not been added
- `trigger` should raise `ValueError` if the machine has no initial state set

## Examples

```python
sm = StateMachine()
sm.add_state("locked")
sm.add_state("unlocked")
sm.add_transition("locked", "coin", "unlocked")
sm.add_transition("unlocked", "push", "locked")
sm.set_initial("locked")

sm.current_state          # "locked"
sm.trigger("coin")        # "unlocked"
sm.current_state          # "unlocked"
sm.get_valid_events()     # ["push"]
```
