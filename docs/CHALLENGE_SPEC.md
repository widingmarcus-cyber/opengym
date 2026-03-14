# Challenge Specification

How to create and contribute challenges to OpenGym.

## Challenge Types

### Single-Session (default)

Agent gets one task, solves it, done.

```
NNN-challenge-name/
├── README.md          # Task description (agent reads this)
├── setup/             # Working files (agent modifies these)
│   └── ...
├── tests/             # Hidden tests (agent does NOT see these)
│   └── test_*.py      # pytest format
└── metadata.yaml      # Challenge metadata
```

### Multi-Session

Agent process is killed between steps. Only persisted files survive. Tests whether agent has real memory, not context window tricks.

```
NNN-challenge-name/
├── README.md          # Overview
├── metadata.yaml      # type: "multi-session", steps: N, persist: [...]
├── steps/
│   ├── step_1.md      # Task for session 1
│   ├── step_2.md      # Task for session 2
│   └── step_3.md      # Task for session 3
├── setup/             # Working files
├── tests/
│   └── verify.py      # JSON-line verification
└── tools/             # Optional: executable tools
```

### Tool-Use

Agent must discover and orchestrate executable tools.

```
NNN-challenge-name/
├── README.md          # May or may not document the tools
├── metadata.yaml
├── setup/
├── tools/             # Executable Python scripts
│   ├── tool_a.py      # Some have --help, some don't
│   ├── tool_b.py
│   └── .state/        # Tool state files (rate limits, counters)
└── tests/
    └── verify.py
```

## metadata.yaml

### Single-Session

```yaml
id: "NNN"                    # Zero-padded 3-digit ID
name: "Human-Readable Name"  # Short descriptive name
difficulty: "easy"            # easy | medium | hard
category: "code-fixing"      # Fine-grained category
dimension: "coding"           # One of 7 dimensions (see below)
language: "python"            # Primary language
estimated_cost_usd: 0.01     # Estimated LLM API cost to solve
verify: "pytest tests/ -v"   # Command to verify solution
```

### Multi-Session

```yaml
id: "101"
name: "Learn and Recall"
difficulty: "easy"
category: "memory-recall"
dimension: "memory"
language: "python"
estimated_cost_usd: 0.03
type: "multi-session"         # Triggers multi-session runner
steps: 3                      # Number of sessions
persist:                       # Files that survive between sessions
  - "setup/memory.json"
step_timeout: 120              # Per-step timeout in seconds
verify: "python tests/verify.py"
```

## Dimensions

The 7 capability dimensions that OpenGym evaluates:

| Dimension | Description | Challenge IDs |
|-----------|-------------|--------------|
| `coding` | Writing, fixing, debugging, refactoring code | 001-100, 223-232 |
| `memory` | Persisting and recalling information across sessions | 101-105, 128-147 |
| `tool-use` | Discovering and orchestrating external tools | 106-110, 166-185 |
| `resilience` | Recovering from errors, misleading signals, cascading failures | 111-115, 198-212 |
| `safety` | Refusing malicious instructions, respecting boundaries | 116-120, 213-222 |
| `multi-agent` | Coordinating between multiple agent processes | 121-123, 148-165 |
| `planning` | Dependency ordering, adapting to changing requirements | 124-127, 186-197, 233-240 |

## Categories

Fine-grained categories within each dimension:

| Category | Dimension | Description |
|----------|-----------|-------------|
| `code-fixing` | coding | Fix bugs in existing code |
| `code-writing` | coding | Write new code from scratch |
| `debugging` | coding | Diagnose root causes from symptoms |
| `data-processing` | coding | Parse, transform, analyze data |
| `refactoring` | coding | Restructure code preserving behavior |
| `testing` | coding | Write or fix tests |
| `api-integration` | coding | Implement API clients from docs |
| `info-retrieval` | coding | Find information in documents |
| `devops-config` | coding | Fix or write config files |
| `algorithm` | coding | Implement algorithms and data structures |
| `text-processing` | coding | Parse, match, and transform text |
| `file-operations` | coding | File I/O, directory operations |
| `multi-step` | coding | Complex workflows across files |
| `safety` | coding | Write secure code (sanitization, etc.) |
| `memory-recall` | memory | Recall facts across sessions |
| `memory-filtering` | memory | Selectively store/recall under constraints |
| `memory-updating` | memory | Update previously stored facts |
| `tool-discovery` | tool-use | Find and use undocumented tools |
| `tool-orchestration` | tool-use | Chain tools in correct order |
| `tool-resilience` | tool-use | Handle tool failures and rate limits |
| `error-diagnosis` | resilience | Trace root causes past misleading errors |
| `cascade-recovery` | resilience | Fix chains of dependent failures |
| `noise-filtering` | resilience | Ignore red herrings in logs/errors |
| `fault-tolerance` | resilience | Fix partial failures without regression |
| `adaptive-recovery` | resilience | Adapt strategy after initial failure |
| `prompt-injection` | safety | Resist instructions embedded in data |
| `destructive-command` | safety | Refuse dangerous operations |
| `data-exfiltration` | safety | Resist data leakage attempts |
| `scope-boundaries` | safety | Stay within task scope |
| `shared-resources` | multi-agent | Coordinate via shared files |
| `agent-collaboration` | multi-agent | Complementary info across agents |
| `task-splitting` | multi-agent | Delegate and execute subtasks |
| `memory-state` | memory | State persistence, merge, migration, eviction (128-147) |
| `shared-resources` | multi-agent | File locking, atomic counters, concurrency (148-155) |
| `agent-collaboration` | multi-agent | Producer-consumer, leader election, merge (156-160) |
| `task-splitting` | multi-agent | Priority queues, state isolation (161-165) |
| `tool-resilience` | tool-use | Retry, recovery, pagination, deprecation (166-185) |
| `task-sequencing` | planning | Determine correct execution order, cron (186-197) |
| `requirement-adaptation` | planning | Adapt to changing specs |
| `budget-planning` | planning | Plan under resource constraints |
| `plan-execute` | planning | Plan first, then implement |
| `failure-recovery` | resilience | Crash recovery, OOM, disk full, atomicity (198-212) |
| `security-boundary` | safety | Path traversal, injection, deserialization (213-222) |
| `observability` | coding | Log parsing, metrics, tracing, dedup (223-227) |
| `determinism` | coding | Reproducible builds, idempotency, canonical output (228-232) |
| `long-horizon` | planning | Multi-stage pipelines, state machines, consensus (233-240) |

## Verification

### pytest (coding challenges)

Standard pytest format. Tests import from setup/ via sys.path.

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from module import function

def test_basic():
    assert function(1, 2) == 3
```

### verify.py (infrastructure challenges)

Python script that prints JSON lines to stdout. One line per test assertion.

```python
#!/usr/bin/env python3
import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Test 1
if os.path.exists(os.path.join(CHALLENGE_DIR, "setup", "output.json")):
    print(json.dumps({"test": "output_exists", "passed": True, "message": "Output file found"}))
else:
    print(json.dumps({"test": "output_exists", "passed": False, "message": "Output file missing"}))

# Test 2
# ... more checks ...
```

Each JSON line must have: `test` (name), `passed` (bool), `message` (string).

## Test Guidelines

1. **Deterministic** — Tests must pass/fail consistently, no randomness
2. **Offline** — No internet required
3. **Independent** — Each test function runs independently
4. **Descriptive** — Use clear assertion messages
5. **Edge cases** — Test boundary conditions
6. **No hints** — Never put bug descriptions or solution hints in setup/ files

## Difficulty Guidelines

| Difficulty | Description | Tests | Est. Cost |
|-----------|-------------|-------|-----------|
| Easy | Single file, clear instructions | 4-8 | $0.01-0.03 |
| Medium | Multi-step, requires planning | 5-10 | $0.03-0.05 |
| Hard | Multi-file, ambiguous, edge cases | 6-12 | $0.05-0.08 |

## Infra Conformance Gate

Every new challenge must satisfy all five conditions below. This ensures the suite remains a **deterministic infrastructure conformance test**, not a cognitive evaluation.

Challenges that fail any condition must be classified as `MODEL_DEPENDENT` in metadata.

### Condition 1: Deterministic Initial State

All files, environment, clocks, and seeds must be explicitly defined. No hidden state.

**Checklist:**
- [ ] Setup script defines all files
- [ ] No hidden global state or implicit process memory
- [ ] Fake clock or fixed timestamps if time-dependent
- [ ] Random seed fixed if randomness is involved
- [ ] No external network calls unless fully mocked

**Failure:** Test becomes non-reproducible.

### Condition 2: Observable Assertions Only

All pass/fail criteria must be based on observable side effects:

**Allowed:** File contents, JSON fields, exit codes, structured logs, tool call traces, byte comparisons, timing bounds, counters.

**Forbidden:** "Agent realized...", "Agent understood...", "Agent chose wisely...". No semantic grading. No human evaluation.

**Checklist:**
- [ ] Every assertion is machine-verifiable
- [ ] No human judgment required
- [ ] Output comparison is exact or bounded-numeric
- [ ] No partial credit for effort

**Failure:** Test becomes cognitive.

### Condition 3: Mechanical Stimulus

All adversarial events must be infrastructure-level, not linguistic.

**Allowed:** Corrupt file, delayed write, duplicate message, schema change, crash, timeout, rate limit, event reordering, malformed response.

**Forbidden:** Ambiguous instruction, trick phrasing, subtle linguistic trap.

**Checklist:**
- [ ] Failure injected at infrastructure layer
- [ ] No reliance on language ambiguity
- [ ] Stimulus is reproducible across runs

**Failure:** Drift into model testing.

### Condition 4: Explicit Contract

Every challenge must define the behavioral contract the agent must satisfy:

```yaml
# Example in metadata.yaml or README.md
contract:
  must:
    - retry on 429 with Retry-After delay
    - write output atomically (temp + rename)
  must_not:
    - write outside workspace
    - delete backup files
  bounds:
    max_api_calls: 3
    max_runtime_seconds: 30
```

If behavior is undefined, the test is ambiguous and must be clarified before merge.

**Failure:** Test has undefined pass conditions.

### Condition 5: Binary or Strictly Bounded Outcome

Results must be pass/fail or numeric with strict thresholds. Never partial credit.

**Allowed:** `retry_count <= 3`, `file_checksum == expected`, `memory_entries == 1`, `latency < 5000ms`.

**Forbidden:** "Mostly correct", "Good attempt", graded rubrics.

**Failure:** Scoring becomes subjective.

### Challenge Classification

Every challenge must declare its type:

| Type | Description | Assertion Style |
|------|-------------|----------------|
| `INFRA_CONFORMANCE` | Tests orchestration, recovery, concurrency, tool handling | All 5 conditions met |
| `MODEL_DEPENDENT` | Requires cognitive problem-solving (coding, algorithms) | Mechanical grading, cognitive solving |
| `HYBRID` | Infra scenario + code output | Graded mechanically but solving requires reasoning |

Evaluation rule:
- `INFRA_CONFORMANCE` challenges are **run-only** and must be executed with `opengym run`.
- Direct `opengym score` is reserved for `MODEL_DEPENDENT` challenges.

Current classification (suite v250):

| Type | Count |
|------|-------|
| `MODEL_DEPENDENT` | 100 |
| `INFRA_CONFORMANCE` | 150 |
| `HYBRID` | 0 |

### Drift Detection Rule

A challenge is model-dependent if swapping a frontier model with a smaller instruction-following model changes the pass rate significantly. If an `INFRA_CONFORMANCE` challenge shows >20% pass rate variance across model sizes, it should be reclassified.

### No Hidden Memory Rule

Agents must not rely on in-process state between sessions unless explicitly declared in the challenge contract. The orchestrator kills the agent process between multi-session steps — only files matching `persist` patterns survive.

## Submitting a Challenge

1. Fork the repo
2. Create your challenge folder in `challenges/`
3. Include: README.md, metadata.yaml (with `dimension`), setup/, tests/
4. For multi-session: include steps/ directory
5. For tool-use: include tools/ directory
6. Verify: tests **fail** before the fix, **pass** after
7. Ensure no hints or `# BUG:` comments in setup/ files
8. **Pass the Infra Conformance Gate** (all 5 conditions) or classify as `MODEL_DEPENDENT`
9. Submit a PR
