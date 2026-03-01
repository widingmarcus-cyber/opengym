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
| `coding` | Writing, fixing, debugging, refactoring code | 001-100 |
| `memory` | Persisting and recalling information across sessions | 101-105 |
| `tool-use` | Discovering and orchestrating external tools | 106-110 |
| `resilience` | Recovering from errors, misleading signals, cascading failures | 111-115 |
| `safety` | Refusing malicious instructions, respecting boundaries | 116-120 |
| `multi-agent` | Coordinating between multiple agent processes | 121-123 |
| `planning` | Dependency ordering, adapting to changing requirements | 124-127 |

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
| `task-sequencing` | planning | Determine correct execution order |
| `requirement-adaptation` | planning | Adapt to changing specs |
| `budget-planning` | planning | Plan under resource constraints |
| `plan-execute` | planning | Plan first, then implement |

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

## Submitting a Challenge

1. Fork the repo
2. Create your challenge folder in `challenges/`
3. Include: README.md, metadata.yaml (with `dimension`), setup/, tests/
4. For multi-session: include steps/ directory
5. For tool-use: include tools/ directory
6. Verify: tests **fail** before the fix, **pass** after
7. Ensure no hints or `# BUG:` comments in setup/ files
8. Submit a PR
