# OpenGym Agent Adapters

Working agent scripts that you can use with `opengym run` out of the box.

## Quick Start

```bash
pip install opengym-ai

# Test the pipeline works (scores 0 — dummy doesn't solve anything)
opengym run 001 --agent "python examples/agents/dummy_agent.py --task '{task}' --dir {workspace}"

# Run with OpenAI (requires OPENAI_API_KEY)
pip install openai
opengym run all --agent "python examples/agents/openai_agent.py --task '{task}' --dir {workspace}" --summary

# Run with Anthropic (requires ANTHROPIC_API_KEY)
pip install anthropic
opengym run all --agent "python examples/agents/anthropic_agent.py --task '{task}' --dir {workspace}" --summary
```

## Adapters

### `dummy_agent.py` — Pipeline Testing

Does nothing. Reads the task, prints workspace info, exits. Use this to verify `opengym run` works before spending API credits.

```bash
opengym run 001 --agent "python examples/agents/dummy_agent.py --task '{task}' --dir {workspace}"
```

### `openai_agent.py` — OpenAI GPT

Agentic loop using OpenAI function calling. Explores the workspace, reads/writes files, executes commands.

**Prerequisites:**
```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

**Usage:**
```bash
# Single challenge
opengym run 001 --agent "python examples/agents/openai_agent.py --task '{task}' --dir {workspace}"

# All challenges with summary
opengym run all --agent "python examples/agents/openai_agent.py --task '{task}' --dir {workspace}" --summary

# Custom model
OPENGYM_MODEL=gpt-4o-mini opengym run 001 --agent "python examples/agents/openai_agent.py --task '{task}' --dir {workspace}"
```

### `anthropic_agent.py` — Anthropic Claude

Same capabilities as the OpenAI agent, using Claude's native tool_use API.

**Prerequisites:**
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

**Usage:**
```bash
# Single challenge
opengym run 001 --agent "python examples/agents/anthropic_agent.py --task '{task}' --dir {workspace}"

# Custom model
OPENGYM_MODEL=claude-haiku-4-5-20251001 opengym run all --agent "python examples/agents/anthropic_agent.py --task '{task}' --dir {workspace}" --summary
```

### Claude Code CLI

If you have Claude Code installed, you can use it directly without a wrapper script:

```bash
opengym run 001 --agent "claude --print --dangerously-skip-permissions 'Read {task} and solve the OpenGym challenge. Only modify files in setup/.' --cwd {workspace}"
```

## How Adapters Work

Each adapter:

1. Receives `--task` (path to task file) and `--dir` (workspace directory)
2. Reads the task description from the file
3. Gives the LLM tools: `read_file`, `write_file`, `list_directory`, `execute_command`, `done`
4. Runs an agentic loop: LLM reads task → calls tools → modifies files → calls `done`
5. All file operations are sandboxed to the workspace directory

The `opengym run` CLI handles everything else: fetching challenges, managing multi-session steps, cleaning workspaces between sessions, scoring results.

## Writing Your Own Adapter

Your adapter just needs to:

1. Accept `--task` (file path) and `--dir` (directory path)
2. Read the task from the file
3. Modify files in the workspace to solve the challenge
4. Exit with code 0

```python
#!/usr/bin/env python3
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--task", required=True)
parser.add_argument("--dir", required=True)
args = parser.parse_args()

task = Path(args.task).read_text()
workspace = Path(args.dir)

# Your agent logic here — read files, call your LLM, write solutions
```

Then run it:
```bash
opengym run all --agent "python my_agent.py --task '{task}' --dir {workspace}" --summary
```
