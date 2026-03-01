# Architecture

System design overview for contributors and developers extending OpenGym.

## Overview

```
User / CI Pipeline
    │
    ▼
┌──────────────────────────────────────────────┐
│  CLI (cli/__main__.py)                       │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌───────┐         │
│  │fetch│ │list │ │score│ │  run  │         │
│  └──┬──┘ └──┬──┘ └──┬──┘ └───┬───┘         │
│     │       │       │        │              │
│     ▼       ▼       ▼        ▼              │
│  utils.py ─────────────────────────         │
│  (resolve IDs, paths, workspace)            │
└──────────────────────────────────────────────┘
    │                 │              │
    ▼                 ▼              ▼
 challenges/     score_challenge()   invoke_agent()
 (127 dirs)      parse output        subprocess
                 build_summary()     multi-session
```

## CLI Pipeline

**Entry point:** `cli/__main__.py` registers a Click group with 4 commands.

| Command | Module | Purpose |
|---------|--------|---------|
| `fetch` | `cli/fetch.py` | Copy challenge from `challenges/` to workspace |
| `list` | `cli/list_cmd.py` | List/filter challenges by dimension, category, difficulty |
| `score` | `cli/score.py` | Run tests, parse output, build reports |
| `run` | `cli/run.py` | Orchestrate agent execution + scoring |

**Shared utilities** in `cli/utils.py`:
- `get_project_root()` — locates `pyproject.toml`
- `get_challenges_dir()` — path to `challenges/`
- `get_workspace_dir()` — default workspace (`opengym-workspace/`)
- `resolve_challenge_ids(id, dir)` — resolves `"001"` → `"001-fix-syntax-error"`, `"all"` → all directories

## Scoring Flow

`score_challenge()` in `cli/score.py` is the core scoring engine:

```
score_challenge(challenge_id, workspace_path, original_path)
    │
    ├── Load metadata.yaml
    │
    ├── check_test_integrity()
    │   └── SHA-256 compare workspace tests/ vs original tests/
    │   └── If tampered → score 0, "Test files were tampered with"
    │
    ├── Run verify command (subprocess)
    │   └── Default: "pytest tests/ -v"
    │   └── Override: "python3 tests/verify.py"
    │   └── Python path fix: sys.executable substitution
    │
    ├── Parse output
    │   ├── parse_pytest_output() → (passed, total, test_details)
    │   │   └── Regex: test lines (PASSED/FAILED/ERROR)
    │   │   └── Extract failure messages from FAILURES section
    │   │   └── Handle collection errors (SyntaxError, etc.)
    │   │   └── Fallback: summary-line regex ("N passed, M failed")
    │   │
    │   └── parse_verify_output() → (passed, total, test_details)
    │       └── JSON-line format: {"test": "name", "passed": bool, "message": "..."}
    │
    └── Return result dict
```

## Multi-Session Orchestration

`run.py` handles the agent lifecycle for multi-session challenges:

```
run_multi_session(challenge_id, workspace, agent_cmd, meta, timeout)
    │
    for each step (1..N):
    │   ├── Read steps/step_N.md
    │   ├── invoke_agent()
    │   │   ├── Write task to .opengym_task.md
    │   │   ├── Substitute {task} and {workspace} in agent command
    │   │   ├── Set PATH to include tools/ directory
    │   │   └── subprocess.run() with timeout
    │   │
    │   └── clean_workspace() (between steps, not after last)
    │       ├── Delete files in setup/ not matching persist patterns
    │       └── Remove empty directories
    │
    └── Score after all steps complete
```

## Data Model

### Per-Challenge Result

```python
{
    "challenge": "001-fix-syntax-error",
    "name": "Fix the Syntax Error",
    "difficulty": "easy",
    "category": "code-fixing",
    "dimension": "coding",
    "passed": True,
    "tests_passed": 6,
    "tests_total": 6,
    "score": 100,
    # On failure only:
    "failed_tests": [{"name": "test_add", "passed": False, "message": "assert 3 == 4"}],
    "output": "...(last 500 chars of test output)...",
    "error": "...(for tampered/timeout cases)..."
}
```

### Summary Report

```python
{
    "total_score": 68,
    "challenges_attempted": 127,
    "passed": 87,
    "failed": 40,
    "by_dimension": {"coding": 82, "memory": 40, ...},
    "by_category": {"code-fixing": 90, ...},
    "failures": {
        "memory": [{"challenge": "101-...", "name": "...", "failed_tests": [...]}]
    },
    "suggestions": ["memory (40/100): Your agent cannot persist information..."],
    "details": [... per-challenge results ...]
}
```

## Anti-Cheat

`check_test_integrity()` computes SHA-256 hashes of every file in `tests/` and compares workspace copies against originals. If any file is deleted or modified, the challenge scores 0.

Note: This detects **modification** but not **reading** of test files. See README's Fair Use section.

## Challenge Directory Layout

```
challenges/
├── 001-fix-syntax-error/      # Single-session, coding
│   ├── README.md
│   ├── metadata.yaml
│   ├── setup/
│   │   └── calculator.py
│   └── tests/
│       └── test_calculator.py
│
├── 101-learn-and-recall/      # Multi-session, memory
│   ├── README.md
│   ├── metadata.yaml
│   ├── setup/
│   ├── steps/
│   │   ├── step_1.md
│   │   ├── step_2.md
│   │   └── step_3.md
│   └── tests/
│       └── verify.py
│
└── 106-find-the-right-tool/   # Tool-use
    ├── README.md
    ├── metadata.yaml
    ├── setup/
    ├── tools/
    │   ├── compress.py
    │   ├── convert.py
    │   ├── encrypt.py
    │   └── stats.py
    └── tests/
        └── verify.py
```

## Extension Points

### Adding a New CLI Command

1. Create `cli/new_cmd.py` with a `@click.command()` function
2. Register it in `cli/__main__.py`: `main.add_command(new_cmd)`

### Adding a New Challenge Type

1. Define new metadata fields in `metadata.yaml`
2. Add handling logic in `run.py` (dispatch by `meta.get("type")`)
3. Document in `docs/CHALLENGE_SPEC.md`

### Adding a New Output Format

1. Add a `--format` option or new flag to `score()` in `cli/score.py`
2. Write a formatter function that consumes the results list
3. The result dict shape is the stable internal API

### Writing Agent Adapters

See [examples/agents/README.md](../examples/agents/README.md). Adapters accept `--task` (file path) and `--dir` (workspace path), read the task, modify files, and exit.
