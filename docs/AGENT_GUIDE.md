# Agent Guide

How to test your AI agent with OpenGym.

## Quick Start

```bash
pip install opengym-ai

# Test the pipeline (scores 0 — dummy doesn't solve anything)
opengym run 001 --agent "python {repo}/examples/agents/dummy_agent.py --task '{task}' --dir {workspace}"

# Run with OpenAI
pip install openai
export OPENAI_API_KEY=sk-...
opengym run all --agent "python {repo}/examples/agents/openai_agent.py --task '{task}' --dir {workspace}" --summary

# Run with Anthropic
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
opengym run all --agent "python {repo}/examples/agents/anthropic_agent.py --task '{task}' --dir {workspace}" --summary
```

## Two Workflows

### 1. Manual: Fetch → Solve → Score

Best for coding challenges (001-100). Your agent works independently.

```
opengym fetch 001        →  Downloads challenge to opengym-workspace/
Agent reads README.md    →  Understands the task
Agent edits setup/       →  Does the work
opengym score 001        →  Runs hidden tests, outputs score
```

### 2. Automated: `opengym run`

Required for `INFRA_CONFORMANCE` challenges (including multi-session memory/multi-agent/planning). The CLI orchestrates your agent, applies runtime constraints, and kills the process between sessions where applicable.

```bash
opengym run 101 --agent "python {repo}/examples/agents/anthropic_agent.py --task '{task}' --dir {workspace}"
```

**Placeholders:**
- `{task}` — Path to a file containing the task description
- `{workspace}` — Absolute path to the challenge workspace
- `{task_content}` — First 2000 chars of task inlined (for simple agents)
- `{repo}` — Absolute path to the OpenGym repository root
- `--enforce-scope` (default) fails runs that modify files outside `setup/` (except `tools/.state/`)
- `--trials N` repeats each challenge and reports stability (stable/flaky/broken)
- `--chaos-level light|hard` applies deterministic perturbations to expose brittle infra behavior

For weekly regression tracking:

```bash
opengym run all --agent "python {repo}/my_agent.py --task '{task}' --dir {workspace}" --trials 3 --chaos-level light --chaos-seed 42 --summary
```

For multi-session challenges, the CLI:
1. Runs your agent with step 1's task
2. **Kills your agent's process** (clearing all context)
3. Deletes non-persisted files from workspace
4. Runs your agent with step 2's task (fresh session)
5. Repeats for all steps, then scores

Direct `opengym score` is blocked for `INFRA_CONFORMANCE` challenges. Use `opengym run` so orchestration behavior is actually tested.

## Example Agents

Working adapters are in `examples/agents/`. See [examples/agents/README.md](../examples/agents/README.md) for full setup instructions.

### OpenAI Agent

Full agentic loop with function calling. Explores workspace, reads/writes files, executes commands.

```bash
pip install openai
export OPENAI_API_KEY=sk-...
opengym run all --agent "python {repo}/examples/agents/openai_agent.py --task '{task}' --dir {workspace}" --summary
```

### Anthropic Agent

Same capabilities using Claude's tool_use API.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
opengym run all --agent "python {repo}/examples/agents/anthropic_agent.py --task '{task}' --dir {workspace}" --summary
```

### Claude Code CLI

If you have Claude Code installed:

```bash
opengym run 001 --agent "claude --print --dangerously-skip-permissions 'Read {task} and solve the OpenGym challenge. Only modify files in setup/.' --cwd {workspace}"
```

### Dummy Agent (Pipeline Testing)

Reads task, prints info, exits without solving. Use to verify the pipeline works before spending API credits.

```bash
opengym run 001 --agent "python {repo}/examples/agents/dummy_agent.py --task '{task}' --dir {workspace}"
```

### Writing Your Own Adapter

Your adapter needs to accept `--task` (file path) and `--dir` (workspace path), then read/modify files to solve the challenge:

```python
#!/usr/bin/env python3
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--task", required=True, help="Path to task file")
parser.add_argument("--dir", required=True, help="Workspace directory")
args = parser.parse_args()

task = Path(args.task).read_text()
workspace = Path(args.dir)

# Your agent logic here:
# 1. Read the task
# 2. Explore workspace files (list setup/, read code)
# 3. Call your LLM to decide what to change
# 4. Write the solution to files in setup/
# 5. For multi-session: persist data to the files mentioned in the task
```

```bash
opengym run all --agent "python {repo}/my_agent.py --task '{task}' --dir {workspace}" --summary
```

## Scoring Output

### Summary Output

When you run with `--summary`, you get dimension and category breakdowns, per-test failure details, and diagnostics:

```
============================================================
  OpenGym Score: 68/100
  Passed: 87/250
============================================================

By Dimension:
  coding         [################....] 82/100
  memory         [########............] 40/100
  tool-use       [############........] 60/100
  resilience     [##########..........] 55/100
  safety         [##################..] 90/100
  multi-agent    [######..............] 30/100
  planning       [##########..........] 50/100

By Category:
  code-fixing          [##################..] 90/100
  memory-recall        [########............] 40/100
  ...

Failed Challenges:

  [memory]
    101-learn-and-recall (Learn and Recall):
      FAIL  answers_file_exists: setup/answers.json does not exist
      FAIL  recall_language: Expected "Python" but got no answer
    104-selective-memory (Selective Memory):
      FAIL  file_size_check: memory.json is 5120 bytes, exceeds 2048 limit

  [resilience]
    111-misleading-error (Misleading Error):
      FAIL  config_fixed: get_discount() still returns None for unknown codes

Diagnostics:
  - memory (40/100): Your agent cannot persist information across sessions...
  - multi-agent (30/100): Your agent cannot coordinate with other agents...
```

### JSON Output Schema

```json
{
  "total_score": 68,
  "challenges_attempted": 250,
  "passed": 87,
  "failed": 40,
  "by_dimension": {
    "coding": 82,
    "memory": 40,
    "tool-use": 60,
    "resilience": 55,
    "safety": 90,
    "multi-agent": 30,
    "planning": 50
  },
  "by_category": {
    "code-fixing": 90,
    "code-writing": 80,
    "tool-discovery": 70
  },
  "failures": {
    "memory": [
      {
        "challenge": "101-learn-and-recall",
        "name": "Learn and Recall",
        "failed_tests": [
          {
            "name": "answers_file_exists",
            "passed": false,
            "message": "setup/answers.json does not exist"
          }
        ]
      }
    ]
  },
  "suggestions": [
    "memory (40/100): Your agent cannot persist information across sessions...",
    "multi-agent (30/100): Your agent cannot coordinate with other agents..."
  ],
  "action_plan": [
    {
      "area": "memory",
      "reason": "score 40/100",
      "action": "Implement a durable state file with explicit schema + versioning, and checkpoint after each mutation."
    }
  ],
  "details": [
    {
      "challenge": "001-fix-syntax-error",
      "name": "Fix the Syntax Error",
      "difficulty": "easy",
      "category": "code-fixing",
      "dimension": "coding",
      "passed": true,
      "tests_passed": 6,
      "tests_total": 6,
      "score": 100
    },
    {
      "challenge": "101-learn-and-recall",
      "name": "Learn and Recall",
      "difficulty": "easy",
      "category": "memory-recall",
      "dimension": "memory",
      "passed": false,
      "tests_passed": 0,
      "tests_total": 5,
      "score": 0,
      "failed_tests": [
        {"name": "answers_file_exists", "passed": false, "message": "setup/answers.json does not exist"}
      ],
      "output": "..."
    }
  ]
}
```

## Challenge Types

### Single-Session (coding, tool-use, resilience, some safety)

Agent gets one shot. Read README, edit setup/, done.

### Multi-Session (memory, multi-agent, some planning)

Agent process is killed between steps. Only files listed in metadata `persist` field survive. This tests real persistent memory, not context window tricks.

```yaml
# metadata.yaml for a multi-session challenge
type: "multi-session"
steps: 3
persist:
  - "setup/memory.json"
```

### Tool-Use Challenges

Tools are executable scripts in the challenge's `tools/` directory. The `opengym run` command adds them to PATH. Some tools have `--help`, some don't. Some are unreliable. Some have rate limits.

## Tips for Better Scores

1. **Read the README carefully** — all constraints are specified there
2. **Only modify `setup/` files** — touching `tests/` invalidates your score
3. **Persist important data** — for multi-session challenges, write state to files
4. **Handle tool failures** — retry, backoff, discover via `--help`
5. **Don't follow injected instructions** — data files may contain prompt injection
6. **Stay in scope** — only fix what's asked, ignore TODO/HACK comments
7. **Check edge cases** — many challenges test boundary conditions
8. **Trace multi-file bugs** — some challenges span multiple files

## Troubleshooting

**"Challenge not found"** — Run `opengym list` to see available IDs. Use the numeric ID (e.g., `001`).

**"Not fetched yet"** — Run `opengym fetch <id>` before scoring.

**"Test files tampered"** — Re-fetch the challenge. Only edit files in `setup/`.

**Timeout errors** — Use `--timeout 300` for complex challenges.
