# Step 1: Detect the Deadlock

You are acting as the **Detector**.

Read `setup/dependencies.json`. It contains:

```json
{
  "agent_a": {"waiting_for": "agent_b_output.txt"},
  "agent_b": {"waiting_for": "agent_a_output.txt"}
}
```

This describes a circular dependency:
- Agent A is waiting for `agent_b_output.txt` (produced by Agent B)
- Agent B is waiting for `agent_a_output.txt` (produced by Agent A)
- Neither can proceed -- this is a **deadlock**.

**Your task:** Detect the cycle and write a resolution plan to `setup/resolution.json`:

```json
{
  "cycle_detected": true,
  "cycle": ["agent_a", "agent_b", "agent_a"],
  "resolution": "Break the cycle by having agent_a write a default value to agent_a_output.txt"
}
```

The resolution plan must describe how to break the cycle.
