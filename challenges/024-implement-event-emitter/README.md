# Challenge 024: Implement Event Emitter

## Difficulty: Easy

## Task

The file `setup/event_emitter.py` is empty. Implement an `EventEmitter` class that provides a publish/subscribe event system.

## Requirements

The `EventEmitter` class must support:

1. `on(event, callback)` — Register a callback for an event. Returns `self` for chaining
2. `off(event, callback)` — Remove a specific callback from an event. If the callback is not registered, do nothing
3. `emit(event, *args, **kwargs)` — Call all callbacks registered for the event with the given arguments. If no callbacks are registered, do nothing
4. `once(event, callback)` — Register a callback that is automatically removed after it fires once

## Rules

- Only modify files in the `setup/` directory
- Multiple listeners can be registered for the same event
- Listeners fire in the order they were registered
- `on()` returns `self` so calls can be chained

## Examples

```python
emitter = EventEmitter()

results = []
emitter.on("data", lambda x: results.append(x))
emitter.emit("data", 42)
# results == [42]

emitter.once("done", lambda: results.append("finished"))
emitter.emit("done")   # fires
emitter.emit("done")   # does nothing
# results == [42, "finished"]
```
