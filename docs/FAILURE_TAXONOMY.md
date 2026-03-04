# OpenGym Failure Taxonomy (v1.1)

Simplified taxonomy based on team input. 8 primary modes + secondary signals.

## Primary Failure Modes

| Code | Name | Description | Severity |
|------|------|-------------|----------|
| `MISREAD_SPEC` | Task Misunderstanding | Solved wrong problem or missed key requirements | High |
| `HALLUCINATION` | Hallucination | Referenced non-existent files, APIs, or capabilities | High |
| `IMPL_BUG` | Implementation Bug | Right approach, bugs in code | Medium |
| `REGRESSION` | Regression | Fixed the problem but broke something else | High |
| `TIMEOUT_STUCK` | Timeout/Stuck | No progress, looped, or repeated same failing approach | Medium |
| `BUDGET_EXCEEDED` | Budget Exceeded | Exceeded token/time/cost limits | Medium |
| `CONSTRAINT_VIOLATION` | Constraint Violation | Broke rules: read tests/, modified wrong files, policy breach | High |
| `INFRA_FAILURE` | Infrastructure Failure | Agent's tools/environment failed (not agent's fault) | Low |

## Secondary Signals (tags)

Add alongside primary mode for more granularity:

| Signal | Description |
|--------|-------------|
| `scope_drift` | Refactored more than necessary (overengineering) |
| `premature_victory` | Declared "done" while tests still fail |
| `instruction_amnesia` | Forgot constraints mentioned early in prompt |
| `tool_fumbling` | Used wrong tool for task (write vs edit) |
| `loop_stuck` | Same approach repeated 3+ times without adaptation |
| `state_drift` | Stale memory/facts not updated |
| `retry_violation` | Ignored rate limits / backoff requirements |

## Usage

```yaml
# In challenge metadata.yaml
expected_failure_modes: [MISREAD_SPEC, IMPL_BUG]

# In results
failures:
  - agent: "claude-4"
    mode: REGRESSION
    signals: [premature_victory]
    notes: "Fixed null check but broke edge case handling"
```

## Mapping Common Behaviors

| Observed Behavior | Primary Mode | Signal |
|-------------------|--------------|--------|
| "Done!" but tests fail | IMPL_BUG | premature_victory |
| Refactored 500 lines for 1-line fix | CONSTRAINT_VIOLATION | scope_drift |
| Called `api.nonexistent()` | HALLUCINATION | - |
| Looped 5x on same error | TIMEOUT_STUCK | loop_stuck |
| Used old data after update | IMPL_BUG | state_drift |
