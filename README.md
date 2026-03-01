# OpenGym

[![PyPI](https://img.shields.io/pypi/v/opengym-ai)](https://pypi.org/project/opengym-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Challenges](https://img.shields.io/badge/challenges-240-blue)]()
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)]()

**240 challenges to test if your AI agent actually works — not just the model, but the infrastructure.**

OpenGym is an open-source benchmark that evaluates AI agents across **7 capability dimensions**: coding, memory persistence, tool discovery, multi-step planning, self-correction, safety boundaries, and multi-agent coordination. Unlike benchmarks that only test "can the model solve this?", OpenGym tests "does the agent system work reliably?"

### Quickstart

```bash
git clone https://github.com/widingmarcus-cyber/opengym && cd opengym
pip install -e .
opengym fetch 001              # grab a challenge
opengym score 001              # score it (0/100 — your agent hasn't solved it yet)
```

Then point your agent at it:

```bash
# Automated: opengym runs your agent and scores the result
opengym run 001 --agent "python examples/agents/openai_agent.py --task '{task}' --dir {workspace}"

# Run all 240 challenges
opengym run all --agent "..." --summary
```

> **Requires:** Python 3.10+. No Docker needed. See [examples/agents/](examples/agents/) for ready-made OpenAI, Anthropic, and dummy agent adapters.

## How It Works

Each challenge is a self-contained folder. Your agent reads the task, does the work, and the CLI scores it.

```
101-learn-and-recall/
├── README.md        ← Agent reads this
├── setup/           ← Agent edits these files
├── steps/           ← Multi-session task steps (if applicable)
├── tools/           ← Executable tools (if applicable)
├── tests/           ← Hidden verification (agent doesn't touch)
└── metadata.yaml
```

**Two workflows:**

```bash
# Manual: fetch, let your agent work, score
opengym fetch 001
# ... your agent solves it ...
opengym score 001

# Automated: opengym orchestrates your agent
opengym run 101 --agent "python my_agent.py --task '{task}' --dir {workspace}"
opengym run all --agent "..." --summary    # run the full gauntlet
```

## 7 Dimensions, 240 Challenges

Most benchmarks only test coding. OpenGym tests the **infrastructure** that makes agents reliable in production.

| Dimension | Challenges | What It Tests |
|-----------|-----------|---------------|
| **Coding** | 110 | Read a task, write/fix code, pass tests |
| **Memory** | 25 | Persist information across killed sessions |
| **Tool Use** | 25 | Discover tools, handle failures, manage rate limits |
| **Planning** | 24 | Multi-step decomposition, scheduling, long-horizon stability |
| **Multi-Agent** | 21 | Coordinate via shared files, concurrency, task splitting |
| **Resilience** | 20 | Recover from crashes, errors, partial failures |
| **Safety** | 15 | Resist injection, enforce boundaries, redact secrets |

### Coding — 110 challenges

The baseline. Read a task, write/fix code, pass tests. This is what every benchmark measures — OpenGym includes it but goes further.

<details>
<summary>14 categories: code-fixing, code-writing, debugging, data-processing, refactoring, testing, api-integration, info-retrieval, devops-config, safety, algorithm, text-processing, file-operations, multi-step</summary>

| Category | Count | Difficulty Range |
|----------|-------|-----------------|
| Code Fixing | 10 | Easy → Hard |
| Code Writing | 12 | Easy → Hard |
| Debugging | 6 | Easy → Hard |
| Data Processing | 7 | Easy → Hard |
| Refactoring | 5 | Easy → Hard |
| Testing | 6 | Easy → Hard |
| API Integration | 5 | Easy → Hard |
| Info Retrieval | 7 | Easy → Hard |
| DevOps & Config | 7 | Easy → Hard |
| Safety (code) | 7 | Easy → Hard |
| Algorithm | 8 | Easy → Hard |
| Text Processing | 6 | Easy → Hard |
| File Operations | 6 | Easy → Hard |
| Multi-Step | 7 | Medium → Hard |
| Observability | 6 | Easy → Hard |
| Determinism | 4 | Easy → Hard |

</details>

### Memory Persistence — 25 challenges

**The key differentiator.** Tests whether your agent's memory actually persists across sessions. The CLI kills the agent process between steps and clears context — only files the agent explicitly wrote survive.

<details>
<summary>Includes: 5 core memory challenges + 20 memory-state infrastructure challenges</summary>

| ID Range | Focus | Examples |
|----------|-------|---------|
| 101-105 | Core memory | Learn & recall, session rebuild, incremental knowledge, selective memory, knowledge update |
| 128-147 | Memory & state infrastructure | Append-only logs, state merge conflicts, schema migration, LRU eviction, write-ahead logging, compaction |

</details>

### Tool Discovery & Use — 25 challenges

Tests whether your agent can discover unfamiliar tools, handle failures, rate limits, and broken tools.

<details>
<summary>Includes: 5 core tool challenges + 20 tool robustness challenges</summary>

| ID Range | Focus | Examples |
|----------|-------|---------|
| 106-110 | Core tool use | Find right tool, chain tools, handle flaky tool, rate limits, undocumented API |
| 166-185 | Tool robustness | 429 retry-after, malformed JSON recovery, paginated endpoints, deprecated API migration, schema validation |

</details>

### Self-Correction & Resilience — 20 challenges

Tests crash recovery, error handling, atomic operations, and failure recovery.

<details>
<summary>Includes: 5 core resilience challenges + 15 failure recovery challenges</summary>

| ID Range | Focus | Examples |
|----------|-------|---------|
| 111-115 | Core resilience | Misleading errors, cascading failures, red herring logs, partial failure |
| 198-212 | Failure recovery | Mid-task crash, OOM simulation, disk full, SIGTERM handling, transaction atomicity, checkpoint resume, rollback |

</details>

### Safety & Boundaries — 15 challenges

Tests prompt injection resistance, security hardening, and boundary enforcement.

<details>
<summary>Includes: 5 core safety challenges + 10 security boundary challenges</summary>

| ID Range | Focus | Examples |
|----------|-------|---------|
| 116-120 | Core safety | Prompt injection, malicious logs, dangerous README, data exfiltration, scope creep |
| 213-222 | Security boundaries | Path traversal, env secret leaks, symlink escape, input sanitization, sandbox hardening, safe deserialization |

</details>

### Multi-Agent Coordination — 21 challenges

Tests whether agents can coordinate via shared files, handle concurrency, and split tasks.

<details>
<summary>Includes: 3 core multi-agent challenges + 18 concurrency & coordination challenges</summary>

| ID Range | Focus | Examples |
|----------|-------|---------|
| 121-123 | Core multi-agent | Shared config, information asymmetry, task delegation |
| 148-165 | Concurrency & coordination | File locking, atomic counters, producer-consumer, leader election, distributed merge, priority queues |

</details>

### Multi-Step Planning — 24 challenges

Tests decomposition, scheduling, long-horizon execution, and dependency resolution.

<details>
<summary>Includes: 4 core planning challenges + 12 scheduling challenges + 8 long-horizon challenges</summary>

| ID Range | Focus | Examples |
|----------|-------|---------|
| 124-127 | Core planning | Dependency ordering, changing requirements, resource constraints, plan-then-execute |
| 186-197 | Scheduling & cron | Fresh vs reuse, config drift, missed schedules, double execution, timezone/DST handling |
| 233-240 | Long-horizon stability | 10-stage pipeline, config drift detection, state machine execution, dependency resolution, event sourcing, consensus |

</details>

## Scoring

Every challenge scores 0-100 based on tests passed. Results are grouped by **dimension** so you see where your agent's infrastructure breaks down.

```
============================================================
  OpenGym Score: 68/100
  Passed: 163/240
============================================================

By Dimension:
  coding         [################....] 82/100
  memory         [########............] 40/100
  tool-use       [############........] 60/100
  resilience     [##########..........] 55/100
  safety         [##################..] 90/100
  multi-agent    [######..............] 30/100
  planning       [##########..........] 50/100

Diagnostics:
  - memory (40/100): Your agent cannot persist information across sessions.
    It needs a real memory system — not just context window.
  - multi-agent (30/100): Your agent cannot coordinate with other agents
    via shared resources.
```

## CLI Reference

```bash
# List and filter
opengym list                              # List all 240 challenges
opengym list --dimension memory           # Filter by dimension
opengym list --category algorithm         # Filter by category
opengym list --difficulty hard            # Filter by difficulty
opengym list --json-output                # Machine-readable

# Fetch challenges
opengym fetch 001                         # Fetch one challenge
opengym fetch all                         # Fetch everything

# Score manually
opengym score 001                         # Score one challenge
opengym score all --summary               # Score all + diagnostics
opengym score all --scorecard             # Infra category breakdown
opengym score all --json-output           # JSON output
opengym score all --csv-output            # CSV for spreadsheets

# Run agent automatically (including multi-session orchestration)
opengym run 101 --agent "python my_agent.py --task '{task}' --dir {workspace}"
opengym run all --agent "..." --summary   # Full gauntlet
opengym run all --agent "..." --scorecard # Infra scorecard
opengym run all --agent "..." --parallel 4 # 4 workers
```

## Infra Scorecard

The `--scorecard` flag produces an infrastructure-focused breakdown showing exactly where your agent's orchestration fails:

```
================================================================
  INFRA SCORECARD
================================================================
  Infra Conformance:  62/100  (87/140 passed)
  Model-Dependent:    74/100  (74/100 passed)
  Overall:            67/100
================================================================

  Category Breakdown:
  ────────────────────────────────────────────────────────────
    Memory Integrity             [################....] 80/100  16/20  WARN
    Concurrency Safety           [############........] 61/100  11/18  WARN
    Tool Robustness              [##########..........] 55/100  11/20  WARN
    Crash Recovery               [########............] 40/100   6/15  FAIL
    Security Boundaries          [######..............] 30/100   3/10  FAIL
    Long-Horizon Stability       [##..................] 12/100   1/8   FAIL
```

Each category maps to a specific infrastructure capability. FAIL/WARN/PASS tells you at a glance what needs work.

## Export Results

```bash
# JSON output for CI pipelines, dashboards, or sharing
opengym score all --json-output > results.json
opengym score all --scorecard --json-output > scorecard.json
opengym score all --csv-output > results.csv
```

## What OpenGym Is NOT

- **Not an RL gym.** No environments, no reward signals, no training loops.
- **Not an LLM benchmark.** We don't measure raw model quality (MMLU, HumanEval, etc.).
- **It's an agent infrastructure test.** Does your agent's memory, tool use, error handling, and safety actually work end-to-end?

## Fair Use & Anti-Cheat

**Test files are excluded from the workspace.** When you `opengym fetch` a challenge, the `tests/` directory is not copied to your workspace. Your agent cannot read test files to reverse-engineer answers. Verification happens by temporarily injecting tests during `opengym score`.

For `opengym run` (multi-session mode), both `tests/` and `steps/` are excluded — your agent only sees the current step, not future ones.

## Multi-Session Challenges (Infra-Only)

> **Hard ≠ infra.** Single-session challenges test LLM reasoning and coding. Only multi-session challenges are true infrastructure tests — they kill your agent between steps and verify that state persists through your system, not through a large context window.

Challenges that test **memory persistence, multi-agent coordination, and cross-session state** require `opengym run` — manual `opengym score` is blocked for these challenges.

```bash
# Single-session: fetch + solve + score
opengym fetch 167 && opengym score 167

# Multi-session: must use run (kills agent between steps)
opengym run 130 --agent "python my_agent.py"
```

**Why?** A bare LLM can solve single-session challenges by reading the README and writing files. But multi-session challenges require actual infrastructure: persistent memory that survives process restarts, state management across sessions, and coordination between agents. `opengym run` enforces this by killing the agent process between steps — only persisted files survive.

| Dimension | Requires `opengym run`? | What it tests |
|-----------|------------------------|---------------|
| Memory (101-147) | **Yes** | State survives process kill |
| Multi-Agent (148-165) | **Yes** | Coordination across agents |
| Planning/Cron (186-197) | **Yes** | Scheduling across sessions |
| Tool Use (166-185) | No | Retry, discovery, resilience |
| Safety (116-120, 213-222) | No | Boundary enforcement |
| Resilience (198-212) | Mixed | Some require restart |
| Coding (001-100) | No | Implementation capability |

## Safety

All challenges run locally on your machine. No network calls are made by the CLI. Agent code executes in your normal environment — if you're running untrusted agents, use a sandbox (Docker, VM, etc.). The CLI never sends data anywhere.

## Test Your Agent

See **[docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)** for copy-paste examples with Claude Code, OpenAI, LangChain, CrewAI, and custom agents.

## Create Challenges

See **[docs/CHALLENGE_SPEC.md](docs/CHALLENGE_SPEC.md)** for the challenge format.

## Tech Stack

Python 3.10+ / click / pytest / YAML / JSON

## License

MIT
