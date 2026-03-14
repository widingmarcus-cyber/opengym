# Installation

## Quick Install (from source)

```bash
git clone https://github.com/widingmarcus-cyber/opengym && cd opengym
pip install -e .
```

## PyPI Install

```bash
pip install opengym-ai
```

Note: PyPI installs the CLI only. Challenges live in the git repo, so clone the repo to access them.

## Development Install

```bash
git clone https://github.com/widingmarcus-cyber/opengym && cd opengym
pip install -e .
```

Dependencies (installed automatically):
- `click>=8.0` — CLI framework
- `pyyaml>=6.0` — metadata parsing
- `pytest>=7.0` — test execution

## Agent Prerequisites

### OpenAI Agent

```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

### Anthropic Agent

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

### Claude Code CLI

Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) separately. No additional pip packages needed.

```bash
opengym run 001 --agent "claude --print --dangerously-skip-permissions 'Read {task} and solve the challenge.' --cwd {workspace}"
```

## Platform Notes

- **Python 3.10+** required (uses `X | Y` union syntax)
- Tested on: **Linux** (Ubuntu), **macOS**, **Windows 11**
- All paths use `pathlib` for cross-platform compatibility
- Subprocess calls use `shell=True` (works on all platforms)
- Windows: long path support may need enabling for deeply nested challenge directories

## Verifying Installation

```bash
opengym --version          # Should print version
opengym list               # Should list 250 challenges
opengym fetch 001          # Downloads challenge to opengym-workspace/
opengym score 001          # Runs tests (will score 0 — nothing solved yet)
```

## Troubleshooting

**"command not found: opengym"**
Ensure you installed in your active virtual environment, or that your pip scripts directory is on PATH.

**ImportError or ModuleNotFoundError**
Check Python version: `python --version` (must be 3.10+).

**"Challenge not found"**
Use the numeric ID: `opengym fetch 001`, not `opengym fetch fix-syntax-error`.

**Timeout errors**
Use `--timeout 300` for complex challenges: `opengym score 001 --timeout 300`.

**Windows: "python3 not found"**
The CLI auto-detects the current Python interpreter. If running challenges manually, use `python` instead of `python3`.
