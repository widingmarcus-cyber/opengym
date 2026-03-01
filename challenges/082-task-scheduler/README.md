# Challenge 082: Task Scheduler

## Difficulty: Hard

## Task

The file `setup/scheduler.py` contains a stub. Implement a `TaskScheduler` class that schedules tasks respecting dependency constraints and priority ordering.

## Requirements

The `TaskScheduler` class must support:

1. `add_task(name: str, priority: int, dependencies: list[str] = None, duration: int = 1)` -- Add a task with a given priority (higher number = higher priority), optional list of dependency task names, and a duration.
2. `schedule() -> list[str]` -- Return an optimal execution order for all tasks. Tasks must appear after all their dependencies. Among tasks whose dependencies are all satisfied, schedule the highest priority task first. Raise `ValueError` if there are circular dependencies.
3. `get_critical_path() -> list[str]` -- Return the critical path: the longest chain of dependent tasks by total duration. If there are ties, return any valid critical path.
4. `total_duration() -> int` -- Return the total duration if tasks are executed sequentially in the scheduled order.

## Rules

- Only modify files in the `setup/` directory
- Tasks added as dependencies must also be added via `add_task` before calling `schedule()`
- Priority only matters when choosing among tasks whose dependencies are already met

## Examples

```python
s = TaskScheduler()
s.add_task("compile", priority=3, duration=2)
s.add_task("test", priority=2, dependencies=["compile"], duration=3)
s.add_task("lint", priority=1, duration=1)
s.schedule()          # ["compile", "test", "lint"] or ["compile", "lint", "test"]
                      # (lint has no deps, but test depends on compile)
s.total_duration()    # 6
s.get_critical_path() # ["compile", "test"]
```
